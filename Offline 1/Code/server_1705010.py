from email import message
from aes_1705010 import *
from rsa_1705010 import *
# first of all import the socket library
import socket,pickle,os   
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")      


key = "BUET CSE17 Batch"
text = "CanTheyDoTheirFest"

# do aes encryption on text
hexStrAra, fillerCount, _ , _=  AESEncrypt(128, text , key)

# generate keys for RSA
keyLength = 32
p1 , p2 = generatePrimes(keyLength//2)
publicKey , privateKey = generateKeyPair(p1,p2)

print("public key : ", publicKey)
print("private key : ", privateKey)

# write private key to file
privateKeyFileName = "DoNotOpenThis/private.key"
os.makedirs(os.path.dirname(privateKeyFileName), exist_ok=True)
with open(privateKeyFileName, "wb") as f:
    pickle.dump(privateKey, f)

# do RSA on key, make encrypted key
encryptedKey = RSAEncrypt(publicKey, key)
 
# a forever loop until we interrupt it or
# an error occurs
while True:
 
  # Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )

  # send [ cipher length ]
  c.send(str(len(hexStrAra)).encode())

  # send [ ciphers ]
  for i in range(len(hexStrAra)):
    message = ''.join(hexStrAra[i])
    print(message)
    c.send(message.encode())
 
  # send [ filler count ] used for padding
  c.send(str(fillerCount).encode())
  print("filler count : ", fillerCount)

  # send [ encrypted key ]
  encryptedKeyString = pickle.dumps(encryptedKey)
  c.send(encryptedKeyString)
  print("encrypted key : ", encryptedKey)

  # send [ public key ]
  publicKeyString = pickle.dumps(publicKey)
  c.send(publicKeyString)
  print("public key : ", publicKey)

  # Close the connection with the client
  c.close()
   
  # Breaking once connection closed
  break