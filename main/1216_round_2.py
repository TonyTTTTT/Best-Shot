from main.models import User, Img, Comment, Classification, UserProfile

img = Img.objects.get(id__exact='201912172259008379')
print(img.cmpScore)