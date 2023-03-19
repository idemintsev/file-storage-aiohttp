async def check_user(username: str, password: str) -> bool:
    if username and password:
        return True
    return False
