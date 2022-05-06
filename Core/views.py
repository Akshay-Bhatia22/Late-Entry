from django.http.response import Http404
from rest_framework import mixins, status, generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from Core.models import Student
from Core.models import LateEntry
from django.utils import timezone
import datetime
# ---------Serializers--------
from Core.serializers import LateEntrySerializer, StudentRecordSerializer, StudentIDSerializer

def check_date(date):
    n = timezone.now()
    # specific_date
    new_datetime = datetime.datetime(date[0], date[1], date[2], n.hour, n.minute, n.second, n.microsecond, n.tzinfo)
    # specific date should be earlier to today as entries at a future date can't be marked
    if n >= new_datetime:
        # print('entered date is past')
        return new_datetime
    else:
        return False
        # return Response({'message':'Future date entries can\'t be marked'}, status=status.HTTP_400_BAD_REQUEST)

def new_check_date(date):
    n = timezone.now()
    current = n.today().date()
    existing = date.date()
    print(current,existing)
    if current >= existing:
        new_datetime = datetime.datetime(date[0], date[1], date[2], n.hour, n.minute, n.second, n.microsecond, n.tzinfo)
        return new_datetime
    else:
        return False


def already_registered(std):
    try:
        existing = std.late_entry.last().created_at.date()
        current = timezone.now().today().date()
        if current==existing:
            return True
    except:
        return False


class Scan(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        try:
            std = Student.objects.get(st_no=data['st_no'])
            if not already_registered(std):
                LateEntry.objects.create(student=std)
                serializer = StudentIDSerializer(std)
                return Response({'message':'Late entry registered entered', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print('no')
                return Response({'message':'Late entry already registered'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except:
            return Response({'message':'Student data doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)


# specific date entry allowed in manual entry only
class ManualEntry(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        st_no_list = data['st_no_list']

        success = 0

# REFACTOR : move date check outside for loop as it is fixed for all student numbers provided
        for i in st_no_list:
            try:
                std = Student.objects.get(st_no=i)
                if not already_registered(std):
                    print("new registration")
                    if not 'date' in data:
                        print("date not provided")
                        LateEntry.objects.create(student=std)
                    else:
                        print("date provided")
                        specific_date=check_date(data['date'])
                        if specific_date:
                            LateEntry.objects.create(student=std, created_at=specific_date)
                        else:
                            return Response({'message':'Future date entries can\'t be marked'}, status=status.HTTP_400_BAD_REQUEST)
                    success += 1
                else:
                    print("new registration")
            
            except:
                pass
        
        return Response({'message':f'{success} Late entry registered {len(st_no_list) - success} failed.'}, status=status.HTTP_201_CREATED)
    
class Record(APIView):
    def get(self, request, format=None):
        std = Student.objects.all()
        serializer = StudentRecordSerializer(std, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
