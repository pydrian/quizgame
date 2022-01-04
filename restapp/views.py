from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Game, User, Question, Answer, Rank
from .serializers import GameSerializer, UserSerializer, QuestionSerializer, AnswerSerializer
from .auth import get_current_user
from .validators import Validator


class GameCRUD(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get game list"""

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        """Create game"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        validator = Validator()
        validator.map_field('name', str, True, 2, 50)
        validated = validator.validate(request.data)

        new_game = Game.objects.create(**validated)
        serializer = GameSerializer(new_game, many=False)

        return Response(serializer.data)

    
    def put(self, request):
        """Update game"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            gameid = int(request.query_params['gameid'])

        except KeyError:
            return Response(
                {"details": "Query parameter `gameid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "Query parameter `gameid` must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validator = Validator()
        validator.map_field('name', str, False, 2, 50)
        validated = validator.validate(request.data)

        upd_game = Game.objects.filter(gameid=gameid).update(**validated)

        if not upd_game:
            return Response(
                {"details": "Game not found"}
            )

        return Response(
            {"details": "Game updated"},
            status=status.HTTP_200_OK
        )


    def delete(self, request):
        """Delete game"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            gameid = request.query_params['gameid'][0]
        except (KeyError, IndexError):
            return Response(
                {"details": "Query parameter `gameid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        del_game = Game.objects.filter(gameid=gameid).delete()

        if not del_game[0]:
            return Response(
                {"details": "Game not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "Game deleted"},
            status=status.HTTP_200_OK
        )


class QuestionCRUD(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get questions"""
        
        try:
            gameid = request.query_params['gameid'][0]
        except (KeyError, IndexError):
            return Response(
                {"details": "Query parameter `gameid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quests = Question.objects.filter(game_id=gameid)
        serializer = QuestionSerializer(quests, many=True)

        return Response(serializer.data)
        

    def post(self, request):
        """Create question"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            gameid = int(request.query_params['gameid'])
        
        except KeyError:
            return Response(
                {"details": "Query parameter `gameid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "Query parameter `gameid` must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validator = Validator()
        validator.map_field('question', str, True, 1, 250)
        validator.map_field('points', int, True, allowed=[5, 10, 15])
        validated = validator.validate(request.data)
        validated['game_id'] = gameid

        try:
            quest = Question.objects.create(**validated)
        except IntegrityError:
            return Response(
                {"details": "Inexistent game with provided gameid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = QuestionSerializer(quest, many=False)
        return Response(serializer.data)


    def put(self, request):
        """Update question"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessbile with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            quest_id = int(request.query_params['questid'])

        except KeyError:
            return Response(
                {"details": "Query parameter `questid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response(
                {"details": "Query parameter `questid` must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validator = Validator()
        validator.map_field('question', str, False, 1, 250)
        validator.map_field('points', int, False, allowed=[5, 10, 15])
        validator.map_field('game_id', int, False)
        validated = validator.validate(request.data)

        try:
            quest_upd = Question.objects.filter(questid=quest_id).update(**validated)

        except IntegrityError:
            return Response(
                {"details": "Inexistent game with provided game_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not quest_upd:
            return Response(
                {"details": "Question not found"},
                status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "Question updated"},
            status=status.HTTP_200_OK
        )


    def delete(self, request):
        """Delete question"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessbile with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            quest_id = request.query_params['questid'][0]
        except (KeyError, IndexError):
            return Response(
                {"details": "Query parameter `questid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        del_quest = Question.objects.filter(questid=quest_id).delete()

        if not del_quest[0]:
            return Response(
                {"details": "Question not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "Question deleted"},
            status=status.HTTP_200_OK
        )


class AnswerCRUD(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Gets all answers"""

        try:
            questid = request.query_params['questid'][0]

        except(KeyError, IndexError):
            return Response(
                {"details": "Query parameter `questid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        answer = Answer.objects.filter(quest_id=questid)
        serializer = AnswerSerializer(answer, many=True)

        return Response(serializer.data)


    def post(self, request):
        """Add new answer"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            questid = int(request.query_params['questid'])
        
        except KeyError:
            return Response(
                {"details": "Query parameter `questid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "Query parameter `questid` must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validator = Validator()
        validator.map_field('variant', str, True, 1, 80)
        validator.map_field('status', bool, True)
        validated = validator.validate(request.data)
        validated['quest_id'] = questid

        try:
            answer = Answer.objects.create(**validated)
        
        except IntegrityError:
            return Response(
                {"details": "Inexistent question with provided questid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AnswerSerializer(answer, many=False)
        return Response(serializer.data)


    def put(self, request):
        """Update answer"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessbile with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            choiceid = int(request.query_params['choiceid'])

        except KeyError:
            return Response(
                {"details": "Query parameter `choiceid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "Query parameter `choiceid` must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validator = Validator()
        validator.map_field('quest', int, False)
        validator.map_field('variant', str, False, 1, 80)
        validator.map_field('status', bool, False)
        validated = validator.validate(request.data)

        try:
            Answer.objects.filter(choiceid=choiceid).update(
                **validated
            )
        
        except IntegrityError:
            return Response(
                {"details": "Inexistent question with provided questid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {"details": "Answer updated"},
            status=status.HTTP_200_OK
        )


    def delete(self, request):
        """Delete answer"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            choiceid = int(request.query_params['choiceid'])
        
        except KeyError:
            return Response(
                {"details": "Query parameter `choiceid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "choiceid must be integer value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        del_answer = Answer.objects.filter(choiceid=choiceid).delete()

        if not del_answer[0]:
            return Response(
                {"details": "Answer not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "Answer deleted"},
            status=status.HTTP_200_OK
        )

class ManageUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Gets all users"""
        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"}
            )
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        """Add new user"""
        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        validator = Validator()
        validator.map_field('username', str, True, 8, 15)
        validator.map_field('password', str, True, 8, 20)
        validator.map_field('email', 'email', True)
        validator.map_field('first_name', str, False, 2, 30)
        validator.map_field('last_name', str, False)
        validator.map_field('is_staff', bool, False)
        validated = validator.validate(request.data)
        
        user = User.objects.create_user(
            **validated
        )

        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)

    
    def delete(self, request):
        """Delete user"""

        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessible with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            userid = int(request.query_params['id'])

        except KeyError:
            return Response(
                {"details": "Query parameter `id` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "id must be integer value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        del_user = User.objects.filter(id=userid).delete()

        if not del_user[0]:
            return Response(
                {"details": "User not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "User deleted"},
            status=status.HTTP_200_OK
        )


    def put(self, request):
        """Update user"""
        current_user = get_current_user(request)
        if not current_user.is_superuser:
            return Response(
                {"details": "Accessbile with administrator privileges"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            userid = int(request.query_params['id'])

        except KeyError:
            return Response(
                {"details": "Query parameter `id` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "id must be integer value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        validator = Validator()
        validator.map_field('username', str, False, 8, 15)
        validator.map_field('password', str, False, 8, 20)
        validator.map_field('email', 'email', False)
        validator.map_field('first_name', str, False, 2, 30)
        validator.map_field('last_name', str, False)
        validator.map_field('is_staff', bool, False)
        validated = validator.validate(request.data)

        upd_user = User.objects.filter(id=userid).update(**validated)

        if not upd_user:
            return Response(
                {"details": "User not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"details": "User updated"},
            status=status.HTTP_200_OK
        )


class Play(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Add choice"""

        current_user = get_current_user(request)
        try:
            choiceid = int(request.query_params['choiceid'])
        
        except KeyError:
            return Response(
                {"details": "Query parameter `choiceid` is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValueError:
            return Response(
                {"details": "choiceid must be integer value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_answer = Answer.objects.get(choiceid=choiceid)
        current_question = Question.objects.get(questid=current_answer.quest_id)
        current_game = Game.objects.get(gameid=current_question.game_id)
        correct_answer = Answer.objects.filter(quest_id=current_question.questid, status=True)

        if current_answer.status:
            points = current_question.points
        else:
            points = 0
        
        Rank.objects.create(
            user = current_user,
            game = current_game,
            quest = current_question,
            points = points
        )

        return Response(
            {
                "answer_status": current_answer.status,
                "points": points,
                "correct_answer_id": correct_answer.first().choiceid,
                "correct_answer": correct_answer.first().variant
            },
            status=status.HTTP_200_OK
        )


class Points(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get current user points"""
        current_user = get_current_user(request)

        ranks = Rank.objects.filter(user_id=current_user.id)
        points_total = 0
        for rank in ranks:
            points_total += rank.points

        return Response(
            {
                "points_total": points_total 
            },
            status=status.HTTP_200_OK
        )


class RankView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get users rank by game"""

        try:
            game_id = request.query_params['game_id']
        except KeyError:
            game_id = None
        
        current_user = get_current_user(request)
        
        if game_id:
            answers = Rank.objects.filter(game_id=game_id, user_id=current_user.id)
            correct_answers_count = 0
            total_answers = 0
            for ans in answers:
                total_answers += 1
                if ans.points:
                    correct_answers_count += 1
            if not total_answers:
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

            return Response(
                {
                    "game_id": game_id,
                    "total_answers": total_answers,
                    "correct_answers_count": correct_answers_count
                },
                status=status.HTTP_200_OK
            )            

        answers = Rank.objects.filter(user_id=current_user.id)
        total_answers = 0
        correct_answers_count = 0
        for ans in answers:
            total_answers += 1
            if ans.points:
                correct_answers_count += 1
        return Response(
            {
                'total_answers': total_answers,
                'correct_answers_count': correct_answers_count
            },
            status=status.HTTP_200_OK
        )
