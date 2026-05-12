from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import authenticate_user, create_access_token, get_current_user
from app.schemas.auth import LoginRequest, TokenResponse, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль.",
        )
    return TokenResponse(
        access_token=create_access_token(user["username"], user["role"]),
        username=user["username"],
        role=user["role"],
    )


@router.get("/me", response_model=UserRead)
def me(user: dict[str, str] = Depends(get_current_user)) -> dict[str, str]:
    return user

