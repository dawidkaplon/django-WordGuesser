from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import renderers, views, status, request

from .serializers import WordSerializer
from .models import Word
from mysite.views import Game

# Create your views here.


class GetWord(views.APIView):
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    def get(self, request, length):
        webscraper = Word()
        webscraper.fetch_data(length)

        if webscraper.word is not None:
            if request.accepted_renderer.format == "json":
                serializer = WordSerializer(webscraper)
                return JsonResponse(
                    {"word": serializer.data}, status=status.HTTP_201_CREATED
                )

            if request.accepted_renderer.format == "html":
                word = Word(word=webscraper.word, definition=webscraper.definition)
                # word.save()  # Create a found word and save it in the database
                
                request.session['word'] = {'word': word.word, 'definition': word.definition}
                Game.reset_flag = True
                return redirect('/game/')

        else:
            return JsonResponse(
                {"message": "Failure"},
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetWordDetails(views.APIView):
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    def get(self, request, id):
        try:
            word = Word.objects.get(id=id)
        except Word.DoesNotExist:
            word = None
        serializer = WordSerializer(word)

        if request.accepted_renderer.format == "html":
            return Response(
                {"word": word},
                template_name="word_details.html",
                status=status.HTTP_200_OK,
            )

        if request.accepted_renderer.format == "json":
            return JsonResponse({"word": serializer.data}, status=status.HTTP_200_OK)


class GetList(views.APIView):
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    def get(self, request):
        if request.accepted_renderer.format == "json":
            all_words = Word.objects.all()
            serializer = WordSerializer(all_words, many=True)
            return Response({"words": serializer.data}, status=status.HTTP_200_OK)

        if request.accepted_renderer.format == "html":
            all_words = Word.objects.all()
            return Response(
                {"words": all_words},
                template_name="words_list.html",
                status=status.HTTP_200_OK,
            )


class AddWord(views.APIView):
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    def post(self, request):
        serializer = WordSerializer(data=request.data)

        # Save the data
        word = request.data["word"]
        definition = request.data["definition"]

        if serializer.is_valid():
            # Create and save a new Word object with the extracted data
            word = Word(word=word, definition=definition)
            word.save()

            if request.accepted_renderer.format == "html":
                return Response(
                    {"word": serializer.data},
                    template_name="index.html",
                    status=status.HTTP_201_CREATED,
                )

            if request.accepted_renderer.format == "json":
                return JsonResponse(
                    {"word": serializer.data}, status=status.HTTP_201_CREATED
                )
