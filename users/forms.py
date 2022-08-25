from django import forms
from . import models


class LoginForm(forms.Form):

    """email과 password를 작성하는 form"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):

    """user모델의 필드를 가져와서 작성"""

    class Meta:
        model = models.User
        fields = ["email", "username"]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "example@gmail.com"}),
            "username": forms.TextInput(attrs={"placeholder": "RediUser"}),
        }

    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())

    def clean_password1(self):

        # password가 맞는지 확인
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        return password

    def save(self, *args, **kwargs):

        # form에서 데이터를 가져와서 user 오브젝트에 저장
        user = super().save(commit=False)
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()
