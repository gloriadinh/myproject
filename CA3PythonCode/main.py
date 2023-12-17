import json

def menuOption():
  print("@@@@ SUBS @@@@")
  print("1. Inventory Management")
  print("2. Sales Management")
  print("3. Discount Setup")
  print("0. Exit")
  option = int(input("Enter option: "))
  return option

def menuOption2():
  # this Function is to check if order.txt exist before proceeding
  orderDict = {}
  try:
  #this will read the file and check if order.txt exist
    open("order.txt", "r")
  #if the file doesn't exits, it will display an IOError
  except IOError:
  #this will create the file order.txt if it doesn't exist
    with open("order.txt", "a") as file:
      json.dump(orderDict, file, indent=2)

  print("a. Create Order")
  print("b. Cancel Order")
  print("c. Update Order Payment")
  print("d. Update Order Status ")
  print("e. List orders (today) ")
  print("f. Order Enquiry ")
  option = input("Enter option: ")
  return option

def inventoryManagement():
  print("a. Bread & Pastry List")
  print("b. Setup New Pastry")
  print("c. Update Pastry")
  print("d. Re-load Pastry List from File")
  option = input("Enter option: ")
  return option

def menuOption3():
  print("a. Add New Discount")
  print("b. Update Discount")
  print("c. Remove Discount")
  option = input("Enter option: ")
  return option


def loadProducts():
# creates an empty dictonary to store detail on products
  products = {}
  with open("Products.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
      itemCode, itemName, price, status = line.strip().split(',')
      products[itemCode] = {
        'name': itemName,
        'price': float(price),
        'status': status
      }
#this will return the "products"dictionary that contains detail on  loaded product
  return products

def loadDiscounts():
  discounts = {}
  with open("discount.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
      minTotal, discountValue = line.strip().split(',')
      discounts[float(minTotal)] = float(discountValue)

#Creates a dictionary to store the details for sorted Discount
  sortedDiscounts = {}
#this loop is to sort the discount in discount.txt
  for key in sorted(discounts):
    sortedDiscounts[key] = discounts[key]
  return sortedDiscounts

#This function will display information on the Products
def breadAndPastryList(products):
  print("-" * 65)
  print("{:<13}{:<25}{:<15}{:<10}".format("Item Code", "Item Name", "Price",
                                          "Status"))
  print("-" * 65)
  for itemCode, product in products.items():
    print('{:<13}{:<25}{:<15}{:<10}'.format(itemCode, product['name'],
                                            product['price'],
                                            product['status']))


def addNewPastry(products):
  itemName = input('Enter name of pastry: ')
  itemCode = input('Enter pastry code: ')
  price = float(input('Enter price of pastry: '))

  # check if the code already exists in the dictionary
  if itemCode in products:
    print('Pastry code already exists. Please choose a unique code.')
    return

  # update the Products.txt file
  with open('Products.txt', 'a') as f:
    f.write(f'\n{itemCode},{itemName},{price},Available')

  print('New pastry added successfully.')

def updatePastry(products):
  itemCode = input("Enter item code to update: ")
#Checks if the item codes exist in the 'products' dictionary 
  if itemCode not in products:
    print("Pastry not found!")
    return

  current = products[itemCode]
  name = current["name"]
  price = current["price"]
  status = current["status"]
  print(
    f"Current details: Item Code: {itemCode} - {name}, Price: {price}, Status: {status}"
  )
  newPrice = input("Enter New Price (Leave blank to keep current price): ")
  newStatus = input(
    "Enter New Status (Available or Unavailable, leave blank to keep current status): "
  )
  # will update the price if the newPrice is provided
  if newPrice != '':
    products[itemCode]["price"] = float(newPrice)
  # will update the Status if the newStatus is provided
  if newStatus != '':
    products[itemCode]["status"] = newStatus
  #Write the updated products details to the "Products.txt" file
  with open("Products.txt", "w") as file:
    for itemCode, pastry in products.items():
      name = pastry["name"]
      price = pastry["price"]
      status = pastry["status"]
      file.write(f"{itemCode},{name},{price},{status}\n")

# 
def reloadFromFile(products):
  with open("Products.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
      itemCode, itemName, price, status = line.strip().split(',')
      products[itemCode] = {
        'name': itemName,
        'price': float(price),
        'status': status
      }
  print("Pastry re-loaded successfully")

def createOrder(products, discounts):
  orderedItems = {}
#Checking if the Item Code that is entered by the user is in products.txt if not print error message
  while True:
    entry = input("Enter Item and Quantity: ")
    if entry == "x" or entry == "X":
      break
    else:
      itemCode, quantity = entry.strip().split(',')
      if itemCode not in products:
        print("Item " + itemCode + " does not exist")
      elif products[itemCode]["status"] != "Available":
        print("Item " + itemCode + " is unavailable")
      else:
        price = products[itemCode]["price"]
        orderedItems[itemCode] = {
          "itemName": products[itemCode]["name"],
          "quantity": int(quantity),
          "unitPrice": price
        }
#Doing the calculation for amount and total
  total = 0
  for itemCode, orderInfo in orderedItems.items():
    price = orderInfo["unitPrice"]
    quantity = orderInfo["quantity"]
    amount = float(price) * float(quantity)
    total = total + amount

#Check if the total is less than 50, if yes then delivery is $5
  delivery = 0.0
  if total < 50:
    delivery = 5.0

  bestDiscount = 0.0
  for minTotal, discountValue in discounts.items():
    if total > minTotal:
      bestDiscount = discountValue
    else:
      break

#calculation on the total due
  totalDue = 0
  if bestDiscount > 0:
    totalDue = (total + delivery) - ((total + delivery) * (bestDiscount / 100))
  else:
    totalDue = (total + delivery)

#Creating a dictionary called orderInfo
  orderInfo = {
    "orderedItems": orderedItems,
    "subtotal": total,
    "deliveryCost": delivery,
    "itemDiscount": bestDiscount,
    "totalDue": totalDue,
    "paymentPaynowReference": ""
  }
  printOrderedItems(orderInfo)
  printPaymentInfo(orderInfo)
  #Checking if th User wants to continue with their Order
  order = input("Proceed to order (y/n):")
  while True:
  #This will check if the users want proceed or not
    if order == "n" or order == "no" or order == "N":
      print("Order will not be carried out")
      break
    elif order == "y" or order == "yes" or order == "Y":
      address = input("Enter delivery address:")
      name = input("Enter Your Name: ")
      import datetime

#Stores the detail in the dictionary
      orderInfo["deliveryAddress"] = address
      orderInfo["name"] = name
      orderInfo["orderStatus"] = "Pending"
      orderInfo["paymentStatus"] = "Pending"
      
      orderDict = {}
      with open("order.txt", "r") as file:
        orderDict = json.load(file)

# Get the current time in the formet YYYYMMDD 
      today = datetime.datetime.now().strftime('%Y%m%d')
      if today not in orderDict:
        orderDict[today] = []

      order_number = len(orderDict[today]) + 1

# Generating the order id using date and order number
      order_id = f"{today}-{order_number:002}"
      print("Order created and Order ID is ", order_id)
      orderInfo["id"] = order_id

      orderDict[today].append(orderInfo)

      with open("order.txt", "w") as file:
        json.dump(orderDict, file, indent=2)
      break
    else:
      print("Invalid Text and try again:")
      break

def cancelOrder():
  orderId = input("Enter order ID to cancel: ")

  orderDict = {}
  with open("order.txt", "r") as file:
    orderDict = json.load(file)

  orderSplit = orderId.split("-")

# commence a flag if the order is found
  isFound = False
# checking the dictionary if the date exist
  if orderSplit[0] in orderDict:
    for order in orderDict[orderSplit[0]]:
#check if the order id exist
      if order["id"] == orderId:
        isFound = True
# checking the order status
        if order["orderStatus"] == "Pending":
          order["orderStatus"] = "Cancelled"
          print("Order is cancelled successfully")
          break
        elif order["orderStatus"] == "Baking" or order["orderStatus"] == "Complete":
          print("Order is already in Baking or Completed status")
      else:
        continue
  else:
    print("There is no order matching your Order Id")

  if isFound == False:
    print("There is no order matching your Order Id")
  else:
    with open("order.txt", "w") as file:
      json.dump(orderDict, file, indent=2)

def updateOrderPayment():
  orderId = input("Enter order ID: ")

  orderDict = {}
  with open("order.txt", "r") as file:
    orderDict = json.load(file)
# split the order id to extract the date and order number
  orderSplit = orderId.split("-")

# checking the dictionary if the date exist
  isFound = False
  if orderSplit[0] in orderDict:
    for order in orderDict[orderSplit[0]]:
      if order["id"] == orderId:
        isFound = True
        if order["orderStatus"] == "Cancelled":
          print("Order is already cancelled cannot update payment")
        else:
          #Check the status
          if order["paymentStatus"] == "Pending":
            paynowRef = input("Enter your PayNow reference: ")

            order["paymentPaynowReference"] = paynowRef
            order["paymentStatus"] = "Received"
            order["orderStatus"] = "Baking"
            print("Payment received Successfully")
            break
          elif order["paymentStatus"] == "Received":
            print("Payment is already Received")
      else:
        continue
  else:
    print("There is no order matching your Order Id")

  if isFound == False:
    print("There is no order matching your Order Id")
  else:
    with open("order.txt", "w") as file:
      json.dump(orderDict, file, indent=2)

def updateOrderStatus():
  orderId = input("Enter order ID: ")

  orderDict = {}
  with open("order.txt", "r") as file:
    orderDict = json.load(file)

  orderSplit = orderId.split("-")

  isFound = False
  if orderSplit[0] in orderDict:
    for order in orderDict[orderSplit[0]]:
      if order["id"] == orderId:
        isFound = True
        if order["paymentStatus"] == "Pending":
          print("Payment is still Pending")
        elif order["orderStatus"] != "Baking":
          print("Order is not Baking")
        elif order["orderStatus"] == "Cancelled":
          print("Order is already cancelled cannot update status")
        elif order["orderStatus"] == "Baking":
          order["orderStatus"] = "Complete"

          print("Order completed")
          break
      else:
        continue
  else:
    print("There is no order matching your Order Id")

  if isFound == False:
    print("There is no order matching your Order Id")
  else:
    with open("order.txt", "w") as file:
      json.dump(orderDict, file, indent=2)

def listOrderToday():
  import datetime
  orderDict = {}
  with open("order.txt", "r") as file:
    orderDict = json.load(file)

  today = datetime.datetime.now().strftime('%Y%m%d')
  if today in orderDict:
    orderList = orderDict[today]
    completedOrderList = []
    bakingOrderList = []
    pendingOrderList = []
  # categorise the order based on the order status
    for order in orderList:
      if order["orderStatus"] == "Complete":
        completedOrderList.append(order)
      elif order["orderStatus"] == "Baking":
        bakingOrderList.append(order)
      elif order["orderStatus"] == "Pending":
        pendingOrderList.append(order)

  #Printing the complete order for the day
    print("*" * 25)
    print("Completed Order(s)")
    print("*" * 25)
    if (len(completedOrderList) > 0):
      print("{:<15}{:<15}{:<15}{:<10}".format("Order ID", "Order Status", "Payment Status", "Total Payment"))
      for completedOrder in completedOrderList:
        printOrderDetails(completedOrder)
    else:
      print("No Completed Orders for Today")

  #Printing the baking order for the day
    print()
    print("*" * 25)
    print("Baking Order(s)")
    print("*" * 25)
    if (len(bakingOrderList) > 0):
      print("{:<15}{:<15}{:<15}{:<10}".format("Order ID", "Order Status", "Payment Status", "Total Payment"))
      for bakingOrder in bakingOrderList:
        printOrderDetails(bakingOrder)
    else:
      print("No Baking Orders for Today")

    #printing the pending order for the day
    print()
    print("*" * 25)
    print("Pending Order(s)")
    print("*" * 25)
    if (len(pendingOrderList) > 0):
      print("{:<15}{:<15}{:<15}{:<10}".format("Order ID", "Order Status", "Payment Status", "Total Payment"))
      for pendingOrder in pendingOrderList:
        printOrderDetails(pendingOrder)
    else:
      print("No Pending Orders for Today")
  else:
    print("No Orders for Today")

# function to allow user to gt the detials on their order
def enquireOrder():
  orderDict = {}
  orderId = input("Enter order ID: ")
  with open("order.txt", "r") as file:
    orderDict = json.load(file)
  
  orderSplit = orderId.split("-")


  if orderSplit[0] in orderDict:
    for orderInfo in orderDict[orderSplit[0]]:
      if orderInfo["id"] == orderId:
        print("Order ID is "+ orderId)
        print("This Order is for "+orderInfo["name"],"," +orderInfo["deliveryAddress"])
        printOrderedItems(orderInfo)  
        printPaymentInfo(orderInfo)   
        break
  else:
    print("There is no order matching your Order Id")

def printOrderDetails(order):
  print("{:<15}{:<15}{:<15}${:<10.2f}".format(order["id"], order["orderStatus"], order["paymentStatus"], order["totalDue"]))

def printOrderedItems(order):
  print("{:<25}{:<10}{:<10}{:<15}".format("Item", "Qty", "Price", "Amount"))
  for itemCode, orderInfo in order["orderedItems"].items():
    price = orderInfo["unitPrice"]
    quantity = orderInfo["quantity"]
    amount = float(price) * float(quantity)
    print("{:<25}{:<10}${:<10.2f}${:<15.2f}".format(orderInfo["itemName"], quantity, price, amount))

def printPaymentInfo(order):
  print("{:<25}{:<10}{:<10}${:<15.2f}".format("", "", "Subtotal", order["subtotal"]))
  print("{:<25}{:<10}{:<10}${:<15.2f}".format("", "", "Delivery", order["deliveryCost"]))

  print("{:<25}{:<10}{:<10}{:<1}%".format("", "", "Discount", order["itemDiscount"]))
  print("{:<25}{:<10}{:<10}${:<15.2f}".format("", "", "Total Due", order["totalDue"]))

#function to check on irregular discount
def isDiscountIrregular(discount, subtotal, discounts):
  for minTotal, discountValue in discounts.items():
    if discount > discountValue:
      if subtotal < minTotal:
        print("Discount % is higher than ${:.2f}".format(minTotal))
        return True
    else:
      if subtotal > minTotal:
        print("Discount % is lower than ${:.2f}".format(minTotal))
        return True
  return False

def addDiscount(discounts):
  addedDiscount = input("Enter Subtotal and Discount: ")
  subtotalStr, discountStr = addedDiscount.strip().split(',')

  subtotal = float(subtotalStr)
  discount = float(discountStr)

  if subtotal in discounts:
    print("Subtotal already exists")
  else:
    if isDiscountIrregular(discount, subtotal, discounts):
      confirmation = input("Are you sure you want to proceed (y/n)")
      if confirmation == "n" or confirmation == "no" or confirmation == "N":
        print("Discount will not be added")
      elif confirmation == "y" or confirmation == "yes" or confirmation == "Y":
        with open("discount.txt", "a") as file:
          file.write(f"{subtotal},{discount}\n")
        print("Discount has been added")
      else:
        print("Invalid option entered.")
    else:
      with open("discount.txt", "a") as file:
        file.write(f"{subtotal},{discount}\n")
      print("Discount has been added")

# to update the discount
def updateDiscount(discounts):
  print(discounts)
  prompt = input("Please enter which value to update (subtotal/discount): ")

  isDiscountUpdated = False
  if prompt.upper() == "DISCOUNT":
    subtotal = float(input("Enter the Subtotal to update: "))
    if subtotal not in discounts:
      print("Subtotal does not exist")
    else:
      newDiscount = float(
        input("Enter the new Discount for ${:.2f}: ".format(subtotal)))
      if isDiscountIrregular(newDiscount, subtotal, discounts):
        confirmation = input("Are you sure you want to proceed (y/n)")
        if confirmation == "n" or confirmation == "no" or confirmation == "N":
          print("Discount will not be updated")
        elif confirmation == "y" or confirmation == "yes" or confirmation == "Y":
          discounts[subtotal] = newDiscount
          isDiscountUpdated = True
          print("Discount updated successfully")
        else:
          print("Invalid option entered.")
      else:
        discounts[subtotal] = newDiscount
        isDiscountUpdated = True
        print("Discount updated successfully")
  elif prompt.upper() == "SUBTOTAL":
    discount = float(input("Enter the Discount to update: "))

    oldSubtotal = -1
    for minTotal, discountValue in discounts.items():
      if discountValue == discount:
        oldSubtotal = minTotal
        break

    if oldSubtotal == -1:
      print("Discount does not exist")
    else:
      newSubtotal = float(
        input(
          "Enter the new Subtotal for {:.2f}% Discount: ".format(discount)))
      if isDiscountIrregular(discount, newSubtotal, discounts):
        confirmation = input("Are you sure you want to proceed (y/n)")
        if confirmation == "n" or confirmation == "no" or confirmation == "N":
          print("Discount will not be updated")
        elif confirmation == "y" or confirmation == "yes" or confirmation == "Y":
          del discounts[oldSubtotal]
          discounts[newSubtotal] = discount
          isDiscountUpdated = True
          print("Discount updated successfully")
      else:
        del discounts[oldSubtotal]
        discounts[newSubtotal] = discount
        isDiscountUpdated = True
        print("Discount updated successfully")

  if isDiscountUpdated:
    with open("discount.txt", "w") as file:
      for minTotal, discountValue in discounts.items():
        file.write(f"{minTotal},{discountValue}\n")

#function to remove discount
def removeDiscount(discounts):
  subtotal = float(input("Enter the Subtotal to delete: "))
  if subtotal in discounts:
    prompt = input("Are you sure you want to delete? (y/n): ")
    if prompt == "n" or prompt == "no" or prompt == "N":
      print("Discount will not be deleted")
    elif prompt == "y" or prompt == "yes" or prompt == "Y":
      del discounts[subtotal]

      with open("discount.txt", "w") as file:
        for minTotal, discountValue in discounts.items():
          file.write(f"{minTotal},{discountValue}\n")
      print("Discount deleted successfully")
    else:
      print("Invalid option entered.")

def main():
  products = loadProducts()
  discounts = loadDiscounts()

  while True:
    option = menuOption()
    if option == 1:
      option = inventoryManagement()
      if option == "a":
        breadAndPastryList(products)
      elif option == "b":
        addNewPastry(products)
      elif option == "c":
        updatePastry(products)
      elif option == "d":
        reloadFromFile(products)
    elif option == 2:
      option2 = menuOption2()
      if option2 == "a":
        createOrder(products, discounts)
      elif option2 == "b":
        cancelOrder()
      elif option2 == "c":
        updateOrderPayment()
      elif option2 == "d":
        updateOrderStatus()
      elif option2 == "e":
        listOrderToday()
      elif option2 == "f":
        enquireOrder()
    elif option == 3:
      option3 = menuOption3()
      if option3 == "a":
        addDiscount(discounts)
      elif option3 == "b":
        updateDiscount(discounts)
      elif option3 == "c":
        removeDiscount(discounts)
    elif option == 0:
      print("Exiting application...")
      break
    else:
      print("Try Again later:")

main()
