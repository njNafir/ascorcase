from datetime import date, timedelta
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Sum
from .serializers import *
from .models import WinnerRestaurant


class MinimumPostSnippet(object):
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            return Response({"Error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantAPIView(generics.GenericAPIView, MinimumPostSnippet):
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MenuAPIView(generics.GenericAPIView, MinimumPostSnippet):
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VoteAPIView(generics.GenericAPIView, MinimumPostSnippet):
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RestaurantUpdateAPIView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MenuUpdateAPIView(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TodaysMenuAPIView(generics.ListAPIView):
    today = date.today()
    queryset = Menu.objects.filter(
        menu_active_date__year=today.year, 
        menu_active_date__month=today.month, 
        menu_active_date__day=today.day
    ).order_by('id')
    serializer_class = MenuListSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CurrentDayWinnerAPIView(views.APIView):
    def get_menus_for_day(self, day):
        return Vote.objects.filter(
                    create_date__year=day.year, 
                    create_date__month=day.month, 
                    create_date__day=day.day
                    ).values('menu').annotate(
                        Sum('star')).order_by('-star__sum')

    def get_winner_restaurants(self):
        return WinnerRestaurant.objects.order_by(
                                    '-winning_date')[:3]

    def get_restaurant_for_menu(self, menu):
        return Menu.objects.get(id=menu).restaurant

    def get(self, request, *args, **kwargs):
        today = date.today()
        today_voted_menus = self.get_menus_for_day(today)

        today_winner = None

        winner_restaurants = self.get_winner_restaurants()
        total_winners = len(winner_restaurants)
        
        if len(today_voted_menus) >= 1:

            if total_winners == 0 or total_winners == 1:
                today_winner = today_voted_menus[0]

            else:
                for voted_menu in today_voted_menus:
                    restaurant = self.get_restaurant_for_menu(
                        voted_menu['menu'])

                    if restaurant.id == winner_restaurants[0].restaurant.id \
                    and restaurant.id == winner_restaurants[1].restaurant.id:
                        continue
                        message = "There is no winner by condition, "\
                                    "probably there has only one restaurant as "\
                                    "the winner for three consecutive days."
                    else:
                        today_winner = voted_menu

        else:
            message = "There is no vote today."

        if today_winner is None:
            result = {
                'message': message
            }

        else:
            votes = Vote.objects.filter(
                        create_date__year=today.year, 
                        create_date__month=today.month, 
                        create_date__day=today.day,
                        menu=today_winner['menu']
                        ).values(
                            'voter__email', 
                            'star',
                            'review'
                            )

            restaurant = self.get_restaurant_for_menu(
                                            today_winner['menu'])

            menu_info = Menu.objects.filter(
                                    id=today_winner['menu']).values(
                                        'id',
                                        'title',
                                        'description',
                                        'price'
                                    )

            menu_items = MenuItem.objects.filter(
                                        menu=today_winner['menu']
                                    ).values(
                                        'title'
                                    )

            total_vote = len(votes)
            total_star = sum([vote['star'] for vote in votes])

            result = {
                'restaurant_name': restaurant.title,
                'menu_info': menu_info,
                'menu_items': menu_items,
                'votes': votes,
                'total_vote': total_vote,
                'total_star': total_star
            }

            winner_restaurant = WinnerRestaurant.objects.create(
                                                    restaurant=restaurant,
                                                    menu=menu_info['id'],
                                                    total_vote=total_vote,
                                                    total_star=total_star
                                                )

        return JsonResponse({'results': result}, safe=False)
