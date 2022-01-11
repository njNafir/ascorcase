from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Restaurant(models.Model):
    owner = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=52)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MenuManager(models.Manager):
    def set_items(self, menu, menu_items):
        return MenuItem.objects.bulk_create([
            MenuItem(**{
                'menu': menu,
                'title': title
            }) for title in menu_items.split(',')
        ])

    def create(self, **kwargs):
        menu_items = kwargs.pop('items', False)
        menu = self.model(**kwargs)
        menu.save()
        menu.items = self.set_items(menu, menu_items)

        return menu


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='image/', default='image/default/11.jpg')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    menu_active_date = models.DateTimeField(null=True, blank=True)

    objects = MenuManager()
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if Menu.objects.filter(
                restaurant=self.restaurant, 
                menu_active_date__year=self.menu_active_date.year, 
                menu_active_date__month=self.menu_active_date.month, 
                menu_active_date__day=self.menu_active_date.day
        ).exists():
            raise Exception("There should be a menu for each day.")

        return super(Menu, self).save(*args, **kwargs)


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voter = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    star = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0.1)
    review = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Vote for {} by {}".format(self.menu, self.voter)


class WinnerRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    total_vote = models.IntegerField(default=1)
    total_star = models.FloatField(default=0.1)
    winning_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {} of {} is the winner "\
                "with total vote: {}, total star: {}".format(
                    self.winning_date.strftime("%YY-%mm-%dd"),
                    self.menu,
                    self.restaurant,
                    self.total_vote,
                    self.total_star
                )
