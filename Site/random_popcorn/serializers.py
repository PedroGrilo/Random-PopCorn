from rest_framework import serializers

from random_popcorn.models import Movie, Genre, Language, AccountProfile


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Genre
        fields = ['id', 'name']


class LanguagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Language
        fields = ['id', 'country', 'language']


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    languages = LanguagesSerializer(many=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'release_date', 'genre', 'languages', 'plot',
                  'rating_imdb', 'poster']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.release_date = validated_data.get('release_date', instance.release_date)

        for languages_data in validated_data.pop('languages'):
            language = instance.languages.get(pk=languages_data['id'])
            language.country = languages_data['country']
            language.language = languages_data['language']
            language.save()

        instance.plot = validated_data.get('plot', instance.plot)
        instance.rating_imdb = validated_data.get('rating_imdb', instance.rating_imdb)
        instance.poster = validated_data.get('poster', instance.poster)

        return instance

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        genre = Genre.objects.create(**validated_data)
        for genres_data in genres_data:
            Genre.objects.create(**genres_data, genre=genre)
        return genre


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = AccountProfile
        fields = ['id', 'user', 'locality', 'movies', ]
