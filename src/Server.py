import socket
import threading
import time 
import select
from math_quiz import MathQuiz

#Latency calculation function:
def latency_check(conn):
    test_msg="ping"
    start_time=time.time()
    conn.sendall(test_msg.encode())
    data = conn.recv(1024)
    end_time=time.time()
    response_time=end_time-start_time
    return response_time

#Username and Password checking function, to check corresponding log in details stored as hashes.  
def password_check(data,username):
    password=False
    if username=="Natan":
        if data=="39f17ec6ebcf3cec37a06d85dc61882be3898d7573f284b7b41222087b6b6a2c":
            password=True
    if username=="Benjy":
        if data=="d50187dd170f377fe06e9b01c9995bea6c685a371c4772e73d42f5d59b021d4b":
            password=True
    return password

#General function used to send all clients messages.
def broadcast_message(msg):
    for client in clients:
        client.sendall(msg.encode())
        
def receive_message_keyboard(client_socket, timeout):
    client_socket.settimeout(timeout) #Specify maximum amount of time the .recv function will take.
    received=False
    try:
        #Wait for given message:
        data = client_socket.recv(1024)
        return data.decode()
    except socket.timeout:  #timeout period has elapsed without receiving any data.
        # Handle the timeout error
        print("Timeout occurred while receiving data.")
        clients.remove(client_socket)
        return received
    except socket.error as e:
        # Handle other socket errors
        print("Socket error occurred:", str(e)) #prints message as well as error message returned by the exception.
        clients.remove(client_socket)
        return received
    finally:
        client_socket.settimeout(None)  # Reset the socket timeout
        
 #Delay function to calculate each client's respective delay: 
def delays_calc(latencies):
    delays=[]
    max_latency=max(latencies)
    #Max latency - all other latencies provides required delay. 
    for index, value in enumerate(latencies):
        delay= max_latency-latencies[index]
        delays.append(delay)
    return delays

#Function to add all player's connections to clients list.
def client_list(conn):
    lock.acquire()
    try:
        clients.append(conn)
    finally:
        lock.release()

#Function to find if user's answers are correct/incorrect
def evaluate_ans(question,answer):
    result, correct = quiz.evaluate_answer(question, answer)
    return correct

clients=[]
latencies=[]
# Instantiate the MathQuiz class
quiz = MathQuiz()
# Create a lock object for thread synchronization
lock=threading.Lock()

def client_thread_game(conn, addr, barrier):
    print("Connected by", addr)
    printed = False
    answers=[]
    valid_answers=[]
    response_times=[]
    scores=[]

    while True:
        #1. Send Welcome Message to clients:
        start_msg = "Welcome to the Synchronized Math Multiplayer game! \nEnter Username:"
        conn.sendall(start_msg.encode())

        #2. Recieve client's respective Username:
        username = conn.recv(1024).decode('utf-8', errors='ignore')
        print(username)

        #3. Ask for corresponding Password
        if username:
            conn.sendall("Enter Password:".encode())

        #4. Password receive and check:
        data = conn.recv(1024)
        password = password_check(data.decode(),username)
        print(f"Received password from Client: {password}")

        if password:
            #5. Send Correct Message to each thread:
            conn.sendall("Correct!\nGame will begin in 5 seconds once 2 players join".encode())
            #Add the threads that logged in to the list of clients
            client_list(conn)

            #Showing |Barrier functionality:
            current_thread = threading.current_thread().getName()
            print(f"{current_thread} is waiting on barrier...")
            #Barrier ensuring both player's enter the game at the same instant:
            barrier.wait()

            #Start game in 5 seconds.
            time.sleep(5)
        
            num_players = len(clients)
            #Initialize scores; index 0= Player, index 1=Points
            scores = [(i + 1, 0) for i in range(num_players)]

            
            for rounds in range(2):
                #Print Round Number
                print(f"Round number: {rounds+1}")
                # Create a math question
                question = quiz.create_question()
            
                #Protect shared resources between each client, preventing potential conficts and race conditions.
                lock.acquire()
                try:
                
                    for index,client in enumerate(clients):
                        #6. Check the latencies, using function:
                        latency = latency_check(client)
                        #Store the latency
                        latencies.append(latency)
                        #Print the respective latencies for demonstation:
                        print(f"Latency for Player {index+1}: {latency}")
                        #Exit the loop once latencies have been calculated for all clients
                        if len(latencies)==len(clients):
                            break  
                        
                    #Calculate each respective delay from latency values:
                    delays = delays_calc(latencies)
                    
                    #Initialize Response time variables:
                    start_times=[]
                    end_times=[]
                    response_times = [0] * len(clients)  
                    
                    for index, client in enumerate(clients):
                       delay = delays[index]
                       #Print corresponding delay for demonstration:
                       print(f"Delay is {index+1}: {delay}")
                       #Sleep creates required delay.
                       time.sleep(delay)
                       #Store corresponding start time for client.
                       start_times.append(time.time())
                       #7. Send the math question
                       client.sendall(question.encode())
                        
                    print("Question sending process over, should Receive each answer:")
                    #Recieve each client's response:
                    answer_1 = ""
                    answer_2 = ""
                    #Set up a response count for 2 player's
                    responses=0
                    while responses<2:
                        #Monitor the list of clients for incoming responses, 
                        all_responses=select.select(clients,[],[])[0]
                        for conn in all_responses:
                            #8. Receive answers from either user who sent response
                            answer = receive_message_keyboard(conn,60)
                            if answer:
                                for i,client in enumerate(clients):
                                    if conn==clients[i]:
                                        end_time=time.time()
                                        index=clients.index(conn)
                                        response_times[index]=end_time-start_times[index]
                                        if i==0:
                                            answer_1=answer
                                            print(f"Answer {i+1}: {answer_1}")
                                        if i==1:
                                            answer_2=answer
                                            print(f"Answer {i+1}: {answer_2}")
                                responses+=1  
                            
    
                    # Evaluate each user's answer
                    correct=evaluate_ans(question,answer_1)
                    if correct:
                        print(f"Answer from player 1: {correct}")
                    valid_answers.append(correct)

                    correct=evaluate_ans(question,answer_2)
                    if correct:
                        print(f"Answer from player 2: {correct}")
                    valid_answers.append(correct)
                        
                    
                    print("Response times: " ,response_times)
                   
                    #Initialize fastest response and player each round
                    fastest_response_time = float('inf')
                    fastest_player = None
    
                    # Find the fastest response time
                    for index, response_time in enumerate(response_times):
                        if valid_answers[index] and response_time < fastest_response_time:
                            fastest_response_time = response_time
                            fastest_player = index + 1
                    
                    
                    # Give a point to the fastest player with a valid answer
                    if fastest_player is not None and valid_answers[fastest_player - 1]:
                        scores[fastest_player - 1] = (fastest_player, scores[fastest_player - 1][1] + 1)
                        print(f"Player {fastest_player} gets a point!")
    
                    #Create a scoring message and broadcast it to each player
                    score_msg = ""
                    for player, score in scores:
                        score_msg += f"Player {player} score: {score}\n"
                    #9. Broadcast the score message
                    broadcast_message(score_msg)
                    
                    valid_answers.clear()
                    response_times.clear()
                    latencies.clear()
                    start_times.clear()
                    delays.clear()
                    
        
                finally:
                    lock.release() 
            
        else:
            #5. Send password or username is incorrect
            conn.sendall("Incorrect Username or Password! \n".encode())

    print(f"Disconnected from {addr}")
    conn.close()

def start_server_game(game_Host,game_Port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((game_Host, game_Port))
        s.listen()
        #Create a Barrier of 2 threads, for 2 players joining the game
        barrier = threading.Barrier(2)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=client_thread_game, args=(conn, addr,barrier))
            thread.start()
            

if __name__ == '__main__':
   
   game_Host="127.0.0.1"
   game_Port=5000
   start_server_game(game_Host, game_Port)
   