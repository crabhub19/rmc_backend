import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import cloudinary.uploader
from social_django.models import UserSocialAuth

User = get_user_model()

class GoogleLoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        token = request.data.get("access_token")

        if not token:
            return Response({"detail": "No access token provided"}, status=400)

        # Verify token with Google
        google_url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
        google_response = requests.get(google_url)

        if google_response.status_code != 200:
            return Response({"detail": "Invalid Google token"}, status=400)

        google_data = google_response.json()
        email = google_data.get("email")
        first_name = google_data.get("given_name")
        last_name = google_data.get("family_name")
        profile_picture = google_data.get("picture","")

        if not email:
            return Response({"detail": "No email found in Google response"}, status=400)

        # Find or create the user
        user, created = User.objects.get_or_create(email=email, defaults={
            "first_name": first_name,
            "last_name": last_name,
        })
    # Upload image to Cloudinary if user has no image
        if created or not user.image:
            try:
                upload_result = cloudinary.uploader.upload(profile_picture, folder="user_image", public_id=f"user_{user.id}", overwrite=True)
                user.image = upload_result.get("secure_url")  # Store Cloudinary image URL
                user.save()
            except Exception as e:
                return Response({"error": f"Cloudinary upload failed: {str(e)}"}, status=500)
        # Create or update UserSocialAuth entry
        social_auth, _ = UserSocialAuth.objects.get_or_create(
            user=user,
            provider="google-oauth2",
            defaults={"uid": email, "extra_data": {"picture": profile_picture}}
        )
        # Update profile picture in social auth if changed
        if social_auth.extra_data.get("picture") != profile_picture:
            social_auth.extra_data["picture"] = profile_picture
            social_auth.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "created": created,
        })
