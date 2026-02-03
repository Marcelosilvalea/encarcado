"""
Schemas Pydantic para validaÃ§Ã£o e serializaÃ§Ã£o de dados
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================================
# SCHEMAS DE USUÃRIO
# ============================================================================

class UserBase(BaseModel):
    """Schema base para usuÃ¡rio"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema para criaÃ§Ã£o de usuÃ¡rio"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema para atualizaÃ§Ã£o de usuÃ¡rio"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase):
    """Schema de resposta de usuÃ¡rio"""
    id: int
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE AUTENTICAÃ‡ÃƒO
# ============================================================================

class Token(BaseModel):
    """Schema de resposta do token"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema de requisiÃ§Ã£o de login"""
    username: str
    password: str


# ============================================================================
# SCHEMAS DE PRODUTO
# ============================================================================

class ProductBase(BaseModel):
    """Schema base para produto"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_available: bool = True


class ProductCreate(ProductBase):
    """Schema para criaÃ§Ã£o de produto"""
    pass


class ProductUpdate(BaseModel):
    """Schema para atualizaÃ§Ã£o de produto"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema de resposta de produto"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE RESPOSTA GENÃ‰RICOS
# ============================================================================

class MessageResponse(BaseModel):
    """Schema para mensagens de resposta"""
    message: str
    detail: Optional[str] = None