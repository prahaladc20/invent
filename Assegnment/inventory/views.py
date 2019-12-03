from django.shortcuts import render
from rest_framework import status
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from . import serializers

from .models import Inventory,InventoryApproval
from django.contrib.auth.models import User
from .serializers import InventorySerializer,UserSerializer,InventoryApprovalSerializer
from .permissions import IsLoggedInUserOrAdmin,IsAdminUser



class UserViewSet(viewsets.ModelViewSet):
	print("123654895555555555555")
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer
	# authentication_classes = (SessionAuthentication, BasicAuthentication)
 
	# permission_classes = (ReadOnly, )
	print(serializer_class, "serializer_class")
	# authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, )

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create':
			permission_classes = [AllowAny]
		elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
			permission_classes = [IsLoggedInUserOrAdmin]
		elif self.action == 'list' or self.action == 'destroy':
			permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


# Inventory record that has been approved
class InventoryList(APIView):
	# print("lllllllllllllllllllllllll")
	# queryset = Inventory.objects.all()
	# serializer_class = InventorySerializer
	permission_classes = (IsAuthenticated,)
	# authentication_classes = (SessionAuthentication, BasicAuthentication)
 

	@csrf_exempt
	def get(self, request, format=None):
		fetch_data = []
		
		result = Inventory.objects.all()
	
		# serializer_class = serializers.InventorySerializer
		serializers = InventorySerializer(result,many=True)
		# print("-------------",fetch_data)
		return Response(serializers.data)	

	def post(self,request,format=None):
		print("lllllllllllllllllllllllll+++",request.data)

		if (request.user.groups.filter(name = 'Store Manager').exists()):
			print("LLLLLLLLLL",request.data)
			serializer = InventorySerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
			
		else:
			request.data['status'] = 'pending'
			request.data['action'] = 'create'
			serializer = InventoryApprovalSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
		# serializer = InventorySerializer(data=request.data)
		# if serializer.is_valid():
		# 	serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventoryDetail(APIView):
	print("UPDATEEEEEEEEEEEEEEEEEEEEEEEEEEEEe")
	# queryset = Inventory.objects.all()
	# serializer_class = InventorySerializer

	def getMasterObject(self, pk):
		print("PPPPPPPPPPPP")
		try:
			return Inventory.objects.get(pk=pk)
		except Inventory.DoesNotExist:
			raise Http404


	def put(self, request, pk, format=None):
		print("calling update",request.data)
		data = self.getMasterObject(pk)
		
		# data = Inventory.objects.get(pk=pk)
		if (request.user.groups.filter(name = 'Store Manager').exists()):
			print(data.product_id,"aagya")
			serializer = InventorySerializer(data, data=request.data)

			if serializer.is_valid():
				serializer.save()
			return Response(serializer.data)
		else:
			print(data.product_id, "data")
			inputData = {
				 'author' : request.data['author'],
				 'product_name' : request.data['product_name'], 
				 'vendor' : request.data['vendor'],
				 'mrp' : request.data['mrp'],
				 'batch_num' : request.data['batch_num'],
				 'batch_date' : request.data['batch_date'], 
				 'quantity' : request.data['quantity'],
				 'master_id' : data.product_id,
				 'status' : 'pending',
				 'action' : 'update'
				}
			serializer = InventoryApprovalSerializer(data=inputData)
			if serializer.is_valid():
				serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		data = self.getMasterObject(pk)
		print("im comint", request)
		if (request.user.groups.filter(name = 'Store Manager').exists()):
			data.delete()
			return Response()
		else:
			print(data.author.id, "data")
			inputData = {
				 'author' : data.author.id,
				 'product_name' : data.product_name, 
				 'vendor' : data.vendor,
				 'mrp' : data.mrp,
				 'batch_num' : data.batch_num,
				 'batch_date' : data.batch_date, 
				 'quantity' : data.quantity,
				 'master_id' : data.product_id,
				 'status' : 'pending',
				 'action' : 'delete'
				}
			print(inputData, "input wala data")
			serializer = InventoryApprovalSerializer(data=inputData)
			if serializer.is_valid():
				serializer.save()
			return Response(serializer.data)
		return Response(status=status.HTTP_204_NO_CONTENT)


# Inventory record pending for approval
class InventoryListApproved(APIView):
	
	permission_classes = (IsAuthenticated,)
	# authentication_classes = (SessionAuthentication, BasicAuthentication)
 

	@csrf_exempt
	def get(self, request, format=None):
		print("pending for approval")
		fetch_data = []
		
		print("pending for approval lllllllllllllllllllllllll",request.user.groups.values_list('name',flat = True))

		result = InventoryApproval.objects.all()
		print("result",result)
		# serializer_class = serializers.InventorySerializer
		serializers = InventoryApprovalSerializer(result,many=True)
		# print("-------------",fetch_data)
		return Response(serializers.data)	

	def post(self,request,format=None):
		print("lllllllllllllllllllllllll+++",request.data)

		if (request.user.groups.filter(name = 'Store Manager').exists()):
			print("LLLLLLLLLL",request.data)
			serializer = InventorySerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			request.data['status'] = 'pending'
			request.data['action'] = 'create'
			serializer = InventoryApprovalSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
		# serializer = InventorySerializer(data=request.data)
		# if serializer.is_valid():
		# 	serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventoryManagerApproval(APIView):
	
	def get_object(self, pk):
		print("PPPPPPPPPPPP")
		try:
			return InventoryApproval.objects.get(pk=pk)
		except InventoryApproval.DoesNotExist:
			raise Http404

	def getMasterObject(self, pk):
		print("PPPPPPPPPPPP")
		try:
			return Inventory.objects.get(pk=pk)
		except Inventory.DoesNotExist:
			raise Http404

	def post(self,request,format=None):
		print("hello+++",request.data)

		if not (request.user.groups.filter(name = 'Store Manager').exists()):
			context = {'message':'Sorry! You are not a manager'}
			return Response(context)
			
		else:
			snippet = self.get_object(request.data['product_id'])
			if (request.data['status'] == 'Approved') : 
				print("LLLLLLLLLL",request.data)
				inputData = {
				 'author' : request.data['author'],
				 'product_name' : request.data['product_name'], 
				 'vendor' : request.data['vendor'],
				 'mrp' : request.data['mrp'],
				 'batch_num' : request.data['batch_num'],
				 'batch_date' : request.data['batch_date'], 
				 'quantity' : request.data['quantity'] 
				}
				# Create Master Inventory
				master = InventorySerializer(data=inputData)
				if master.is_valid():
					master.save()

				# Update Inventory-approval	
				print(snippet, "snippet")
				approval = InventoryApprovalSerializer(snippet, data=request.data)

				if approval.is_valid():
					# print("Done")
					approval.save()
				return Response(master.data, status=status.HTTP_201_CREATED)
			else:
				print("check me ")
				approval = InventoryApprovalSerializer(snippet, data=request.data)
				if approval.is_valid():
					approval.save()
			return Response(status=status.HTTP_201_CREATED)

		return Response(status=status.HTTP_400_BAD_REQUEST)

	
	def put(self, request, pk, format=None):


		snippet = self.get_object(pk)
		
		masterSnippet = self.getMasterObject(snippet.master_id)

		if not(request.user.groups.filter(name = 'Store Manager').exists()):
			context = {'message':'Sorry! You are not a manager'}
			return Response(context)

		else:
			master = InventorySerializer(masterSnippet, data=request.data)
			if master.is_valid():
				master.save()

			approval = InventoryApprovalSerializer(snippet, data=request.data)
			if approval.is_valid():
				approval.save()
			return Response(status=status.HTTP_201_UPDATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		print(snippet.master_id, "snippet")
		
		if not(request.user.groups.filter(name = 'Store Manager').exists()):
			context = {'message':'Sorry! You are not a manager'}
			return Response(context)
		else:
			inputData = {
				 'author' : snippet.author.id,
				 'product_name' : snippet.product_name, 
				 'vendor' : snippet.vendor,
				 'mrp' : snippet.mrp,
				 'batch_num' : snippet.batch_num,
				 'batch_date' : snippet.batch_date, 
				 'quantity' : snippet.quantity,
				 'master_id' : snippet.master_id,
				 'status' : 'approved',
				 'action' : 'delete'
				}
			masterSnippet = self.getMasterObject(snippet.master_id)
			print(masterSnippet, "masterSnippet")
			masterSnippet.delete()

			approval = InventoryApprovalSerializer(snippet, data=inputData)
			if approval.is_valid():
				approval.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

class InventoryApprovalAction(APIView):
	print("UPDATEEEEEEEEEEEEEEEEEEEEEEEEEEEEe")
	# queryset = Inventory.objects.all()
	# serializer_class = InventorySerializer

	def get_object(self, pk):
		try:
			return InventoryApproval.objects.get(pk=pk)
		except InventoryApproval.DoesNotExist:
			raise Http404

	def put(self, request, pk, format=None):
		snippet = self.get_object(pk)
		request.data['status'] = 'pending'
		request.data['action'] = 'update'
		serializer = InventoryApprovalSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = InventoryApproval.objects.get(pk=pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)