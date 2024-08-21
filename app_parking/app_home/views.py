from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):

    testimonials = [
        {
            "quote": "The parking service was exceptional! Booking was easy, and finding a spot was a breeze. Highly recommend!",
            "name": "Olena Solovey",
            "position": "Kyiv",
            "image": "c1.jpg",
        },
        {
            "quote": "I've used several parking services, but this one stands out for its reliability and convenience. Great experience!",
            "name": "Mykhailo Tkachenko",
            "position": "Lviv",
            "image": "c2.jpg",
        },
        {
            "quote": "Fantastic service with very user-friendly online booking. I felt my car was safe and secure. Will definitely use again.",
            "name": "Sofiya Kovalenko", 
            "position": "Odesa",
            "image": "c3.jpg",
        },
        {
            "quote": "Efficient and straightforward. The online reservation system saved me a lot of time, and the staff was very helpful.",
            "name": "Yaroslav Petrenko",
            "position": "Kharkiv",
            "image": "c4.jpg",
        },
        {
            "quote": "A top-notch parking solution. The website is easy to navigate, and the parking spots are well-maintained. Very satisfied!",
            "name": "Olha Marchenko",
            "position": "Dnipro",
            "image": "c5.jpg",
        },
        {
            "quote": "Great experience overall. The process was smooth from start to finish, and the staff were courteous and efficient.",
            "name": "Yevhen Sydorenko",
            "position": "Zaporizhzhia",
            "image": "c6.jpg",
        },
        {
            "quote": "I was impressed by the cleanliness and organization of the parking facilities. Booking online was a breeze.",
            "name": "Hanna Zhuravel",
            "position": "Poltava",
            "image": "c7.jpg",
        },
        {
            "quote": "Top-quality service and excellent customer support. The parking spot was exactly as described and very convenient.",
            "name": "Artem Bondarenko",
            "position": "Sumy",
            "image": "c8.jpg",
        },
        {
            "quote": "I had a seamless experience with this parking service. The website was user-friendly, and the parking area was secure.",
            "name": "Alina Shevchenko",
            "position": "Chernihiv",
            "image": "c9.jpg",
        },
        {
            "quote": "The reservation system was fast and easy to use. I felt confident leaving my car here. Highly recommended!",
            "name": "Maksym Kravchuk",
            "position": "Ivano-Frankivsk",
            "image": "c10.jpg",
        },
        {
            "quote": "Excellent service and great value for money. The online booking process was efficient, and the parking spot was perfect.",
            "name": "Mariya Honcharenko",
            "position": "Uzhhorod",
            "image": "c11.jpg",
        },
    ]

    return render(
        request, "app_home/index.html", context={"testimonials": testimonials}
    )


def about_us_detail(request):
    return render(
        request, "app_home/about_index.html", context={"msg": "About Us"}
    )

