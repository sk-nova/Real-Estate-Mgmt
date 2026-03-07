import logging
from typing import Optional

from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)

def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str] = None) -> None:
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime
    }
    
    response.set_cookie("access", access_token, **cookie_settings)
    
    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)
    
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        
        token_response = super().post(request, *args, **kwargs)
        
        if token_response.status_code == status.HTTP_200_OK:
            access_token = token_response.data.get("access")
            refresh_token = token_response.data.get("refresh")
            
            if access_token and refresh_token:
                set_auth_cookies(
                    response=token_response, 
                    access_token=access_token, 
                    refresh_token=refresh_token
                )
                
                token_response.data.pop("access", None)
                token_response.data.pop("refresh", None)
                
                token_response.data["message"] = "Login Successful."
            else:
                token_response.data["message"] = "Login Failed."
                
                logger.error(
                    "Access or Refresh Token not found in login response data"
                )
        return token_response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        
        refresh_token = request.COOKIES.get("refresh")
        
        if refresh_token:
            request.data["refresh"] = refresh_token
        
        refresh_response = super().post(request, *args, **kwargs)
        
        if refresh_response.status_code == status.HTTP_200_OK:
            access_token = refresh_response.data.get("access")
            refresh_token = refresh_response.data.get("refresh")
            
            if access_token and refresh_token:
                set_auth_cookies(
                    response=refresh_response, 
                    access_token=access_token, 
                    refresh_token=refresh_token
                )
                
                refresh_response.data.pop("access", None)
                refresh_response.data.pop("refresh", None)
                
                refresh_response.data["message"] = "Access Token refreshed successfully."
            else:
                refresh_response.data["message"] = "Access or Refresh Token not found in refresh response data"
                
                logger.error(
                    "Access or Refresh Token not found in refresh response data"
                )
        return refresh_response


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        
        provider_response = super().post(request, *args, **kwargs)
        
        if provider_response.status_code == status.HTTP_200_OK:
            access_token = provider_response.data.get("access")
            refresh_token = provider_response.data.get("refresh")
            
            if access_token and refresh_token:
                set_auth_cookies(
                    response=provider_response, 
                    access_token=access_token, 
                    refresh_token=refresh_token
                )
                
                provider_response.data.pop("access", None)
                provider_response.data.pop("refresh", None)
                
                provider_response.data["message"] = "You are logged in successfully."
            else:
                provider_response.data["message"] = "Access or Refresh Token not found in provider response data."
                
                logger.error(
                    "Access or Refresh Token not found in provider response data"
                )
        return provider_response
    

class LogoutAPIView(APIView):
    def post(request: Request, *args, **kwargs) -> Response:
        
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        
        return response