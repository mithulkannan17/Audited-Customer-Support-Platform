from fastapi import Header, HTTPException
from app.security.roles import Role

def require_role(*allowed_roles: Role):
    async def checker(x_role: str = Header(None)):
        if x_role is None:
            raise HTTPException(status_code=401, detail="Missing role")
        
        if x_role not in [r.value for r in allowed_roles]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return x_role
    
    return checker