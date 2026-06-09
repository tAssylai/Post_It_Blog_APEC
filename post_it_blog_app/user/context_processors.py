from post_it.models import Profile

def profile(request):
    if request.user.is_authenticated:
        profile_obj, _ = Profile.objects.get_or_create(user=request.user)
        return {"profile": profile_obj}
    return {}