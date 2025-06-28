from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..forms.auth import EditProfileForm


@login_required
def profile_view(request):
    customer = None
    try:
        customer = request.user.customer
    except:
        pass  # If the Customer object doesn't exist

    return render(
        request,
        "store/profile.html",
        {
            "user": request.user,
            "customer": customer,
        },
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "store/edit_profile.html", {"form": form})
