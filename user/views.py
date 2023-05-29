from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from baseapp import utils
from django.contrib import messages
from account.models import LoginHistory
from .models import *
from .forms import UserUpdateForm, PasswordChangeForm


@login_required
def dash_board(request):
    user = request.user
    try:
        investment = Investments.objects.get(user=user)
    except Investments.DoesNotExist:
        investment = None
    earnings = 0
    if user.referral_bonus == user.balance:
        earnings = user.balance
    else:
        earnings = user.balance - user.referral_bonus
    context = {
        "logs": LoginHistory.objects.filter(user=user).order_by("-date")[:3],
        "investment": investment,
        "earnings": earnings,
    }
    return render(request, "users/index.html", context)


@login_required
def withdrawal_(request):
    user = request.user
    if request.POST:
        accountnum = request.POST.get("accountnum")
        accountname = request.POST.get("accountname")
        bank = request.POST.get("bank")
        amount = int(request.POST.get("amount"))

        if user.balance >= amount:
            bank = Bank.objects.create(
                acc_name=accountname, acc_num=accountnum, ty_pe=bank
            )
            transaction = Transactions.objects.create(
                user=user,
                amount=amount,
                trans_type=utils.W,
                unique_u=utils.trans_code(),
            )
            transaction.bank_details = bank
            user.balance -= amount
            user.save()
            transaction.save()
            messages.success(request, ("ការដកប្រាក់ត្រូវបានដាក់"))
            return redirect("withdrawal")
        else:
            messages.warning(request, ("ថវិកាមិនគ្រប់គ្រាន់!"))
            return redirect("withdrawal")

    return render(request, "users/withdrawal.html")


@login_required
def transactions_(request):
    transactions = Transactions.objects.filter(user=request.user).order_by("-date")
    return render(request, "users/transaction.html", {"transactions": transactions})


@login_required
def settings_(request):
    user = request.user
    if request.POST:
        submit = request.POST.get("submit")
        if submit == "UpdateProfile":
            u_form = UserUpdateForm(request.POST, instance=user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, ("ធ្វើបច្ចុប្បន្នភាពគណនី!"))
                return redirect("settings_")
        # elif submit == "ChangePassword":
        #     p_form = PasswordChangeForm(request.POST,instance=user)
        #     if p_form.is_valid():
        #         password1 = p_form.cleaned_data['password1']
        #         user.set_password(password1)
        #         user.save()
        #         messages.success(request, f'Password Change')
        #         return redirect('settings_')
        else:
            messages.warning(request, f"កំហុសដែលមិនស្គាល់បានកើតឡើង!")
            return redirect("settings_")

    else:
        u_form = UserUpdateForm(instance=user)
        # p_form = PasswordChangeForm(initial={'user_id': user.id})
    return render(request, "users/settings.html", {"u_form": u_form})


@login_required
def change_password_view(request):
    user = request.user
    if request.POST:
        p_form = PasswordChangeForm(request.POST, instance=user)
        if p_form.is_valid():
            password1 = p_form.cleaned_data["password1"]
            user.set_password(password1)
            user.save()
            messages.success(request, f"ការផ្លាស់ប្តូរពាក្យសម្ងាត់")
            return redirect("change_password")
        else:
            messages.warning(request, f"ពាក្យសម្ងាត់មិនត្រូវគ្នាទេ។")
            return redirect("change_password")
    else:
        p_form = PasswordChangeForm(initial={"user_id": user.id})
    return render(request, "users/changepassword.html", {"p_form": p_form})
