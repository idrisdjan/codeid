from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.views import View


class Register(View):
    
    template_name = 'registration/register.html'
    
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)
    
# class Login(View):
    
#     template_name = 'registration/login.html'
    
#     def get(self, request):
#         context = {
#             'form': AuthenticationForm()
#         }
#         return render(request, self.template_name, context)

class LoginUser(View):
    
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def get_context_data(self, *, object_list=None **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    