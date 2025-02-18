💠 What is the Strategy?

✨Connect to Your VPS✨

✨Installing Git & python✨ sudo apt update sudo apt install git sudo apt install python3 && sudo apt install python3-pip

Change the Directory

cd Midas_B0T Install TMUX screen & Install all modules

apt install tmux

tmux new-session -s Midas-TG

pip install -r requirements.txt Now let’s get the INITDATA from TG-miniapp:

🔸 Open Telegram on your PC

🔸Log into your account and open the Midas Miniapp.

🔸Capture init_data Token

🔸Press F12 to open the Developer Tools.

🔸Click on the Console, then paste below command:

console.log(window.Telegram?.WebApp?.initData); 🔸Copy the entire init_data token.

Go back to your VPS & Paste in the auth.txt file.

nano auth.txt 📌If you have multiple accounts, place each token on a new line.

Open proxy.txt file to input Proxy for per Account!

nano proxy.txt Format per line:

socks5://user:pass@IP:PORT 
socks5://user:pass@IP:PORT
http://user:pass@IP:PORT 
http://user:pass@IP:PORT 


Save it and then run B0T!!

python3 main.py CONGRATULATIONS😒

THAT’S IT FOR NOW!!!!😒😒 I hope you have found this thread 🧵 helpful. Thnx for reading my thread.
