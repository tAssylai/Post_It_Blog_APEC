def profile(request):
    if request.user.is_authenticated:
        return {"profile": request.user.profile}
    return {}