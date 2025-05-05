Publication date: 12/77
Volume 11, Issue 2

**Computers: The Secret Behind the Secret Code**
**Author: Not specified**
**Page number(s): 5-6**

Computers: 
The Secret Behind the Secret Code 
With the rapidly decreasing cost of 
sophisticated electronic circuitry, the 
day is not far off when it will be 
financially possible to send informa-
tion by ''electric mail" over public 
channels, instead of the pen-and-
paper medium currently favored by 
the U.S. Postal Service. Recent 
advances in cryptography, the art of 
secret cipher-coding of messages, have 
assured that this mail will only be 
decipherable and readable by its 
intended recipient. The proof of this 
assertion comes from the "purest" 
subjects in mathematics, algebra and 
number theory, as well as the 
theoretical area known as ''cqmpu-
tational complexity". Finally, we will 
all have pre-programmed, special-
purpose personal computers to do 
this enciphering and deciphering, and 
these machines will most likely be 
cheap enough to get free in a box of 
Cheerios. Although this would seem 
to insure perfect equality of security 
for all, in the highest traditions of 
democracy, the U.S. Government is 
extremely upset by the recent break-
throughs in cryptography. It's OK for . 
us, sure. But if the Russians figure 
out how to do it, as the argument 
goes, the National Security Agency 
and their friends, the C.I.A., will be 
unable to keep up with Leonid 
Brezhnev•s latest moves. 

Codes and Keys 
Coding messages is a very old 
business, as is the task of code 
breaking. Caesar made use of what 
are now called "Caesar ciphers" which 
work by cyclically "shifting" the 
letters of the alphabet. A 3-shift, for 
instance, would code the letter A as 
D, 8 as E, and so forth. (A !-shift on 
HAL, the name of the computer in 
the movie 2001, produces IBM. Kinda 
makes you wonder, don't it?) The so-
called "key" to the code is the 
distance of the shift; once that is 
known, the code is broken. 

Another more secure cryptographic 
system is the transmission of private 
key for a specific message. This key 
would be a list of random numbers as 
long as the message to be transmitted. 
The key is delivered to the recipient 
of a message, followed by the message 
itself. The key describes a special 
Caesar cipher for each letter in the 
message. A key 9 4 7 10, for 
example, followed by the message 
LSKO, is deciphered as CODE, since 
counting 9 letters backwards (alpha-
betically) from L yields C, 4 letters 
back from S is 0, and so forth. 

Properly executed, the one-time key 
can only be broken by random 
guessing. This is the cryptographer's 
dream. But there are a lot of other 
difficulties. The amount of corres-
pondence doubles since very long 
keys must be transmitted for each 
message. The key could be intercepted 
and copied before it reaches the 
recipient, and the message decoded 
easily. And if a lot of messages are 
being sent, the problem of syn-
chronizing the proper keys with their 
associated messages becomes very 
complicated. For extended communi-
cations between a large number of 
parties, the one-time key system is a 
hopeless mess. 

One Way Functions 
The inspiration for the first major 
breakthrough in cryptographic re-
search came from Whitfield Diffie 
and Martin Hellman of Stanford 
University. Their work appeared in 
''New Directions in Cryptography" 
(IEEE Transactions on Information 
Theory, November 1976). Diffie and 
Hellman propose a cryptographic 
technique called the "public key 
cryptosystem" which relies on a group 
of-coding functions called "one-way 
trapdoor functions." These functions 
are easy to carry out, but like a 
trapdoor, very difficult to reverse. 
The characteristics for a good one-
way trapdoor function are the 
following: 
1. AD messages are simply coded into 
integers by changing A to 0 I, B to 
02, and so on. T hen we only have 
to "code" and "decode" large 
numbers. 
2. There are two encoding and de-
coding procedures f and g which 
inverses of one another. If a text 
is simply coded into a number N, 
we encode the message by sending 
the number M = f(N), and M is 
decoded by computing g( M) = 
g(f(N)), which (if our coding 
procedures work) must be N. 
Therefore g(f(N)) = N. Since 
encoding and decoding are es-
sentially the same kind of opera-
tion, changing one number to 
another, it is also true that 
f(g(N)) = N. 
3. The encoding and decoding pro-
cedures f and g can both be done 
quickly. 
4. The "trapdoor" condition: Given 
the procedure f, it is compu-
tationally infeasible for anyone to 
break the code and derive g. 

With these conditions, it is easy to 
describe an efficient communications 
system. Every user A who wishes to 
participate in this message sending 
scheme has his own encoding and 
decoding machines. Let's call them fA 
and g,,. User A makes his encoding 
device fA public and sends one to all 
his friends with the following mes-
sage: " If you want to send me some 
electronic mail, type it into vour 
electric message sender and encode it 
with my fA machine just before you 
mail it." His decoding device,gA, 
however, he keeps a secret, so only he 
has a copy of it. This way, no one 
besides A will be able to decode 
messages sent to A. 

Computer Crime and 
Digital Signatures 
The single problem with this design 
is that it is only secure at one end. 
When 8 sends a message to A, it is 
clear that only A can read it. But it is 
still possible that 8 did not send the 
message, for another individual C 
could be impersonating 8 and writing 
messages in B's name. 

It is this loophole that has been 
exploited in an increasingly popular 
public offense known as computer 
crime, namely ripping off with 
machines for fun and profit. An 
excellent summary of such criminal 
exploits can be found in a two-part 
series which appeared in the New 
Yorker this summer ("Annals of 
Crime (Computers - I and II)," 
August 22, 1977 and August 29, 
1977). Consider a bank that has a 
computerized account system. If a 
bank teller can learn to impersonate 
the bank president on the computer, 
the teller can learn the balance of 
special accounts, shift money from 
one account to another (which in-
volves a mere change of numbers 
stored in computer memory), and 
generally make a mess of things. In a 
bank without a C'Omputer system of 
this sort, such activity would be 
impossible. First, the bank teller 
doesn't look like the bank president, 
so personal attempts would obviously 
fail if he tried to ask the accountant 
anything. Second, a written request 
would probably fail, since those in the 
know would see-that rhe signature at 
the bottom of the bank president's 
p\JTported request was not authentic. 
In either case the fraud might easily 
be traced back to the ba nk teller. 

The clever solution to this problem 
of anonymity is what Diffie and 
Hellman call "digital signatures". 
Here is how it works: Suppose B 
wants to send A a message N. B has a 
public encoding device fn (of.which A 
and everyone else has a copy) and a 
secret decoding device gu. Similarly, 
A has a public encoding device fA 
(which 8 knows) and his own 
decoding device gA, also secret. To 
send the message N, B first encodes 
the message with fA, and then codes 
the result with his own device gu, and 
sends the message g8(fA(N)}. When A 
receives the message, he first decodes 
it with B's public coder fR, and then 
gets fA(N), as fH and gu a re mathe-
matical inverses. A then applies his 
private decoding device gA to fA(N). 
and out comes the message N! 

This method is absolutely secure. 
The reason is that when B sent the 
message to A, he used his secret 
coding device gu. For someone to 
impersonate B. they would have to 
figure out how to derive g .. from ftl. 
and this should be next to impossible. 
Coding a message with your own 
th~ MW journal. tkcnrtb~r 6. 1977 
secret g-machine is .a way of .. signing" 
the message, because no one else can 
duplicate that coding procedure. Such 
a public key cryptosystem can resist 
the strongest form of cryptographic 
code breaking, the "chosen plaintext 
attack." 

The secret of the one-way trapdoor 
function is pretty much out of the 
bag. The details of the prime number 
implementation (as mentioned by 
Martin Gardner in the "Mathematical 
Games" section of Scient(fic Amen{ 
can. August 1977) can be found in a 
paper called "On Digital Signatures 
and Public-Key Cryptosystems" 
(Technical Memo 82, April 1977), 
available for 35 cents and a stamped 
addressed envelope by writing to Dr. 
Ronald Rivest, Laboratory for Com-
puter Science, MIT, 545 Technology 
Square, Cambridge, Mass. 02139. 
Yes, for a mere 35 cents, you too can 
create unbreakable codes in the 
privacy of your own home. Don't 
rush for your checkbook, though. At 
last count, Rivest had received on the 
order of two thousand requests for 
this paper, as yet unanswered . Why is 
Professor Rivest such a poor corres-
pondent? Because of the National 
Security Agency. 

The explanation for this state of 
affairs gained public attention in a 
front-page New York Times article 
(October 19, 1977), entitled "Scien-
tists Accuse Agency of Harassment 
Over Code Studies." A source at the 
National Science Foundation, which 
funds much of the research described 
here, complained that NSA was 
engaging in .. syste mati c~ bureaucratic 
sniping" in an attempt to control this 
research. The article appeared a week 
after a conference on information 
theory was held at Cornell University 
in Ithaca, N.Y. 

Several weeks before the con-
ference, its sponsors, the Institute of 
Electric and Electronic Engineers 
(IEEE), received a letter from one of 
its members, J oseph A. Meyer. Ac-
cording to the Times. well-placed 
scientists claim that Meyer is em-
ployed by the NSA. Meyer warned 
that publication and distribution of 
scientific papers on cryptography, 
presented at the upcoming conference, 
would oe in violation of the 1954 
Munitions Control Act, known cur-
rently as the Arms Export Control 
Act. Lawyers from the IEEE, Stan-
ford, and MIT generally concurred 
with this view. Scientific research is 
routinely sent abroad to nations all 
over the world, including the Soviet 
Union. The new research could be 
used to create security systems for 
military communications that would 
be impenetrable by the KGB, the 
Soviet intelligence agency. Of course, 
should the Soviets or any other 
nation employ the same techniques, 
the NSA and C.I.A. would be equally 
unable to break the code. Hence 
publicizing this research is roughly 
synonymous with exporting arma-
ments to the military menace emanat-
ing from Moscow. This set the stage 
for a rather tense conference. 

At the conference, Diffie and 
Hellman presented their results on 
N P problems and their relations to 
cryptography, as briefly described 
above. Rivest of MIT also presented 
the MIT group's results on prime-
number encryption. Under advice 
from MIT lawyers, however, Rivest 
said that he was unable to answer 
questions on the MIT group's re-
search, although he read the paper he 
had prepared for the conference. The 
legal logjam over publication has also