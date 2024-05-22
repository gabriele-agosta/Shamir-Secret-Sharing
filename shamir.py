import random
import numpy as np
import concurrent.futures

from player import *
from dealer import *

def delta(i, Xs, q):
    d = 1
    for j in Xs:
        if j != i:
            d = (d * (-j) * pow((i - j) % q, -1, q)) % q
    return int(d)

def reconstruct(players, i, q):
    secretReconstructed = 0
    Xs = [player.x for player in players]
    for player in players:
        secretReconstructed += delta(player.x, Xs, q) * player.y[i]
    return secretReconstructed 

def rebuildShare(n_players, players, q):
    reconstructedSecret, decryptedSecret = [], ""
    n_shares = len(players[0].y)

    for j in range(n_shares):
        value = reconstruct(players[:n_players + 1], j, q)
        reconstructedSecret.append(value % q)
    decryptedSecret = "".join(chr(c) for c in reconstructedSecret)
    return (n_players + 1, decryptedSecret)

def decrypt(players, dealer):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures, results = [], []
         
        for i in range(len(players)):
            futures.append(executor.submit(rebuildShare, i, players, dealer.q))

        for future in futures:
            results.append(future.result())
        concurrent.futures.wait(futures)
        
    with open('result.txt', 'a') as file:
        for result in results:
            nPlayers, decryptedValue = result
            file.write(f"Reconstructed secret with {nPlayers} = {decryptedValue}\n")

def splitSecret(dealer, player):
    dealer.distributeShares(player)


def encrypt(dealer, players):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(splitSecret, dealer, player) for player in players]
        concurrent.futures.wait(futures)

    
def main():
        n = int(input(f"Choose the number of players: "))
        threshold = int(input(f"Choose the threshold: "))

        dealer = Dealer(threshold)
        players = [Player(i) for i in range(1, n + 1)]
        open('result.txt', 'w').close()

        dealer.chooseSecret()
        dealer.chooseQ()
        dealer.set_polynomials()
        encrypt(dealer, players)
        decrypt(players, dealer)

if __name__ == "__main__":
    main()