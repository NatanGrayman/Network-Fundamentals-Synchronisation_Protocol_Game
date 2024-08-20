import socket
import threading
import time 
import hashlib

#Function which hashes directly the users password, retruned hashed object as hexadecimal.
def password_handle(password):
    password=password.encode()
    hash_object = hashlib.sha256()
    hash_object.update(password)
    hashed_data = hash_object.hexdigest()
    print(hashed_data)
    return hashed_data

#Getting user input from the terminal with a configurable number of retries and a timeout period between retries
def get_user_input_with_retry(max_attempts, timeout):
    attempts = 0
    while attempts < max_attempts:
        try:
            user_input = input()
            return user_input
        except KeyboardInterrupt: #exception occurs (triggered by pressing Ctrl+C),
            raise  # Reraise KeyboardInterrupt to allow the user to exit
        except:
            attempts += 1
            print("Terminal glitch detected. Retrying...")
            time.sleep(timeout)
    #If all retries fail:
    raise Exception("Terminal glitch occurred repeatedly. Exiting.")


def latency_check(s):
    latency_check=s.recv(1024).decode()
    #Only check latency if msg is customized ping, ensuring no 'input' from user.
    if latency_check=='ping':
        s.sendall(latency_check.encode())
        return True
    return False
    
    
def start_client_game(game_host,game_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((game_host,game_port))
        while True:
            # 1. Receiving Welcome Message and request for username:
            msg= s.recv(1024)
            print(f"{msg.decode()}")

            #2. Provide Server with username:
            username=get_user_input_with_retry(2,15)
            s.sendall(username.encode())
            
            #3. Receive message to input password:
            msg= s.recv(1024)
            print(f"{msg.decode()}")
            
            #4. Password input by user,subsequent hash and send
            password= password_handle(input())
            s.sendall(password.encode())
            
            #5.Recieve "Correct" or "Incorrect"
            msg= s.recv(1024)
            print(f"{msg.decode()}")

            #5. Controlling If the client sent the incorrect password:
            if msg.decode()== "Incorrect Username or Password!":
               break

    
            for round_num in range(2):
                if round_num<2:
                    print(f"Round number: {round_num+1}")

                #6. Checking latency
                latency=latency_check(s)

                #Print if latency values were actually sent/received:
                print(f"Sent latency values: {latency}")
                
                
                #7.Receive Math Questions:
                math_question=s.recv(1024).decode()
                print(math_question)
                print(time.time())
                answer=get_user_input_with_retry(2,15)
                s.sendall(answer.encode())
                
                #8. Scores allocation:
                score_msgs=s.recv(1024).decode()
                print(score_msgs)
                
            print("Game Over")
            
        

if __name__ == '__main__':
    i=2
    if i==1:
        game_host="0.tcp.sa.ngrok.io"
        game_port=14544
    if i==2:
        game_host="localhost"
        game_port=5000

    start_client_game(game_host, game_port)