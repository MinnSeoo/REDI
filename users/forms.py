from django import forms
from . import models


class LoginForm(forms.Form):

    """email과 password를 작성하는 form"""

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "이메일"
        self.fields["password"].label = "비밀번호"

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
        username = forms.CharField(max_length=30)
        fields = ("email", "username")
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "example@gmail.com"}),
            "username": forms.TextInput(attrs={"placeholder": "RediUser"}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "이메일"
        self.fields["username"].label = "닉네임"
        self.fields["password"].label = "비밀번호"
        self.fields["password1"].label = "비밀번호 확인"

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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        username = forms.CharField(max_length=30)
        fields = ("avatar", "username", "bio")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "RediUser"}),
            "bio": forms.Textarea(attrs={"placeholder": "당신의 소개를 입력하세요"}),
        }
        labels = {"avatar": "프로필 사진", "username": "닉네임", "bio": "자기소개"}


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"})
    )

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "이메일"

    def clean(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.EMAIL:
                self.add_error(
                    "email", forms.ValidationError("User's login method is not email")
                )
            else:
                return self.cleaned_data
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
