async def check_user(username: str = None, password: str = None) -> bool:
    if username and password:
        return True
    return False
