from asyncio.log import logger
import logging
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from .forms import InquiryForm, PersonalForm
from .models import Sample
from config.settings import *
from config.settings_dev import *
from .models import Colors

import shutil
import os

logger = logging.getLogger(__name__)

class IndexView(generic.FormView):
    template_name = "index.html"
    form_class = PersonalForm

    # postメソッドをオーバーライドする
    def post(self, request, *args, **kwargs):
        form = PersonalForm(request.POST)

        # フォームから受け取ったデータをmodelのフィールドに格納
        sample = Sample()
        sample.gender = request.POST.get('gender', None)
        sample.img = request.FILES['img']
        sample.save()
        img_path = sample.img.url
        

        #性別確認テスト
        print(sample.gender)
        print(img_path)

        #画像判定モデルの使用
        from .pcf_model.main import finder
        try:
            S, contrast = finder("." + img_path)
            print(S, contrast)
        except IndexError:
            return render(request, 'index.html', context={
                'form': self.form_class, 
                'error_message': '※顔を認識できませんでした。\n別の写真でお試しください。',
            })
        except Exception:
            return render(request, 'index.html', context={
                'form': self.form_class, 
                'error_message': '※画像ファイルを読み込めませんでした。\n別の写真でお試しください。',
            })

        
        #モデルで結果をDBから取り出し変数に格納
        ###モデルの呼び出し###
        # from .models import Colors
        # model = Colors
        # colors = get_queryset(self)
        # def get_queryset(self):
        #     colors = Colors.objects.filter(base_type_id=4)
        #     return colors
        
        # def get_queryset(self):
        #     return super().get_queryset()
        
        

        #結果をresult.htmlに送ってHTML生成
        # context={
        #     'colors': colors
        # }
        # return render(request, 'result.html', context)
        # {
        #     #'result': result ,
        #     }
        #)

class ResultView(generic.ListView):
    template_name = "result.html"
    model = Colors
    
    def get_queryset(self):
        return Colors.objects.filter(base_type_id=4)


class InquiryView(generic.FormView):
    template_name = "form.html"
    form_class = InquiryForm
    success_url = reverse_lazy('personal_color:form')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class IntroductionView(generic.TemplateView):
    template_name = "introduction.html"


class LoginView(generic.TemplateView):
    template_name = "login.html"
    

class LogoutView(generic.TemplateView):
    template_name = "signup.html"


class MembersView(generic.TemplateView):
    template_name = "members.html"


class TestView(generic.TemplateView):
    template_name = "403.html"