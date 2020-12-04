from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    DeleteView, UpdateView)

from categories.models import Category
from django.contrib.auth.models import User
from accounts.models import UserProfileInfo
from . import settings

class ListCategory2(ListView):
    model = Category
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all().order_by('pk')[:6]
        return context

from sorl.thumbnail import  get_thumbnail
from resizeimage import resizeimage
class ProfileView(TemplateView):
    template_name = 'profile.html'
    profile_pic = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = UserProfileInfo.objects.filter(
            user = self.request.user
        ).get()

        if current_user.profile_pic:
            profile_pic = True
            picture = current_user.profile_pic
            edited_picture = get_thumbnail(picture, '350x350', quality=99, format='PNG')
        else:
            profile_pic = False
            root = settings.MEDIA_ROOT
            import os
            root1 = os.path.join(root, 'profile_pics/no-image.png')
            picture = root1
            edited_picture = get_thumbnail(picture, '350x350', quality=99, format='PNG')
            # resizeimage.resize_cover(picture, [200, 100], validate=False)
            # rescale_image(picture,width=100,height=100)

        user_info = {
            'user':current_user,
            'picture':edited_picture,
            'profile_pic':profile_pic,
        }

        context['user_info'] = user_info
        return context


class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class IndexView(TemplateView):
    template_name = 'index.html'





#News_paper section
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# for national news of prothom alo
def national_news(request):
    prothom_alo_national = []
    pa_date = []
    pa_links = []
    pa_news_summery = []

    for number in range(1,4):

        url = "https://www.prothomalo.com/bangladesh/article?page="+str(number)
        national_news = requests.get(url)

        national_soup = BeautifulSoup(national_news.content, 'html.parser')
        pa_dates = national_soup.find_all('span',attrs={'class':'time aitm'})
        #pa_dates = [s['data-published'] for s in pa_dates1]
        national_headings = national_soup.find_all('h2',attrs={'class':'title_holder'})
        url_of_news = national_soup.find_all('a', attrs={'class':'link_overlay'})
        summeries = national_soup.find_all('div', attrs={'class':'summery'})

        for headline in national_headings:
            prothom_alo_national.append(headline.text)
        for date in pa_dates:
            pa_date.append(date.text)
        for link in url_of_news:
            pa_links.append(str(link.get('href')))
        for sum in summeries:
            pa_news_summery.append(sum.text)

        prothom_alo = zip(prothom_alo_national, pa_news_summery, pa_date,pa_links)

        #for national news of kalerkontho
        kaler_kontho_national = []
        kl_date = []
        kl_links = []
        kl_news_summery = []

        for number in range(0,3):
            number = number*18
            url = url = "https://www.kalerkantho.com/online/country-news/"+str(number)
            national_news = requests.get(url)

            national_soup = BeautifulSoup(national_news.content, 'html.parser')
            kl_date = national_soup.find('div',attrs={'class':'header-top-bar'}).text
            national_headings = national_soup.find_all('a',attrs={'class':'title'})
            url_of_news = national_soup.find_all('a',attrs={'class':'title'})
            summeries = national_soup.find_all('div', attrs={'class':'col-xs-8 summary'})

            for headline in national_headings:
                kaler_kontho_national.append(headline.text)
            for link in url_of_news:
                kl_links.append(str(link.get('href')).strip('.'))
            for sum in summeries:
                kl_news_summery.append(sum.text)

            kaler_kontho = zip(kaler_kontho_national, kl_news_summery,kl_links)

    return render(request,'newspaper.html', {'prothom_alo':prothom_alo, 'kaler_kontho':kaler_kontho,'kl_date':kl_date, 'is_national':True} )


def sports_news(request):
    #for sports news of prothom alo
    prothom_alo_sports = []
    pa_sports_date = []
    pa_sports_links = []
    pa_sports_news_summery = []

    for number in range(1,3):
        url = "https://www.prothomalo.com/sports/article?page="+str(number)
        sports_news = requests.get(url)

        sports_soup = BeautifulSoup(sports_news.content, 'html.parser')
        pa_dates = sports_soup.find_all('span',attrs={'class':'time aitm'})
        sports_headings = sports_soup.find_all('h2',attrs={'class':'title_holder'})
        url_of_news = sports_soup.find_all('a', attrs={'class':'link_overlay'})
        summeries = sports_soup.find_all('div', attrs={'class':'summery'})

        for headline in sports_headings:
            prothom_alo_sports.append(headline.text)
        for date in pa_dates:
            pa_sports_date.append(str(date.text))
        for link in url_of_news:
            pa_sports_links.append(str(link.get('href')))
        for sum in summeries:
            pa_sports_news_summery.append(sum.text)

        sports_prothom_alo = zip(prothom_alo_sports, pa_sports_news_summery, pa_sports_date, pa_sports_links)

    #for sports news of kalerkontho
    kaler_kontho_sports = []
    kl_sports_date = []
    kl_sports_links = []
    kl_sports_news_summery = []

    for number in range(0,2):
        number = number*18
        url = "https://www.kalerkantho.com/online/sport/"+str(number)
        sports_news = requests.get(url)

        sports_soup = BeautifulSoup(sports_news.content, 'html.parser')
        kl_sports_date = sports_soup.find('div',attrs={'class':'header-top-bar'}).text
        sports_headings = sports_soup.find_all('a',attrs={'class':'title'})
        url_of_news = sports_soup.find_all('a',attrs={'class':'title'})
        summeries = sports_soup.find_all('div', attrs={'class':'col-xs-8 summary'})

        for headline in sports_headings:
            kaler_kontho_sports.append(headline.text)
        for link in url_of_news:
            kl_sports_links.append(str(link.get('href')).strip('.'))
        for sum in summeries:
            kl_sports_news_summery.append(sum.text)

        sports_kaler_kontho = zip(kaler_kontho_sports, kl_sports_news_summery, kl_sports_links)

    return render(request,'newspaper.html', {'prothom_alo':sports_prothom_alo, 'kaler_kontho':sports_kaler_kontho,'kl_date':kl_sports_date, 'is_national':False})
