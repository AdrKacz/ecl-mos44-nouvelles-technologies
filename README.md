# A brief look into cryptocurrencies

In an attempt to understand cryptocurrencies and their impact, I decided to learn how a cryptocurrency is working and to make one myself. Then, I will use my new skills to better understand what is included in the carbon footprint of a transaction.

# Installation

```sh
# macOS
git clone https://github.com/AdrKacz/ecl-mos44-nouvelles-technologies.git
cd ecl-mos44-nouvelles-technologies
python3 -m venv .venv
source .venv/bin/activate
python3 -i main.py
```

> To create a virtual environment in Python on another OS, read the [docs](https://docs.python.org/3/library/venv.html)

# Proof of concept

## Use it!

```py 
alice = Wallet()
bob = Wallet()
marc = Wallet()
sam = Wallet()

marc.send_money(50, alice.public_key)
bob.send_money(23, alice.public_key)
alice.send_money(5, bob.public_key)
```

```
Mining ...
 Solved: 126627
Mining ...
 Solved: 32358
Mining ...
 Solved: 41668

-- 0 --
Block
prev_block_hash : None
transaction
 amount : 100
 payer : 11859374687103049094718306087503599478521517113855481039355975878343188981093985575206365229375879616687381610833980569143319589094874650841836865333365107
 payee : 9900545048987212331789694080921188162843652829003239955282089041830056594178120744033715917651154585506483868770592591892034548896725804565607482668229229

ts : 1642755667.754027
nonce : 752366858


-- 1 --
Block
prev_block_hash : 6af2a02ad4a598dadbfdd26230203b7ac7cc9245af1c8139fef0538c7a179de2
transaction
 amount : 50
 payer : 7498382098256801607687414937197133746131200726872246845140581618288276026275695278736563012075736154685200820494251100906212671900641512429957364175203793
 payee : 6873454529983932499621495886320437326911007884630140969205187980792927504813363457774966243367554865949505212714615799744565874154277269596826219829889367

ts : 1642755667.995132
nonce : 288796334


-- 2 --
Block
prev_block_hash : 83bbf5c0bc6af8b290786245c2f2039102ea1ae25b7d18507bf8d0ca374082c9
transaction
 amount : 23
 payer : 7720599026921224053496329366194900160412846328960872101466632495753786215067747679871889365117709744729781770274481686901500147644497061837147306590002093
 payee : 6873454529983932499621495886320437326911007884630140969205187980792927504813363457774966243367554865949505212714615799744565874154277269596826219829889367

ts : 1642755668.212825
nonce : 867077390


-- 3 --
Block
prev_block_hash : 71584b29f9d8044d4098970b8c73139426e08e8a4ab5240677e69ba9c1044d64
transaction
 amount : 5
 payer : 6873454529983932499621495886320437326911007884630140969205187980792927504813363457774966243367554865949505212714615799744565874154277269596826219829889367
 payee : 7720599026921224053496329366194900160412846328960872101466632495753786215067747679871889365117709744729781770274481686901500147644497061837147306590002093

ts : 1642755668.267565
nonce : 191947455
```

## How does it work?

### How can I start using it?

First, you need to create a `Wallet`. This `Wallet` handles your **private key** and your **public key**.

Your **private key** will sign your `Transaction`, to prove that you are the one who made them.

Signature is a bidirectional mechanism that uses one **key** to sign a message, and another **key** to verify that the message was signed with the first one. As you may guess, both **keys** are deeply linked.

> Singing use [RSA algorithm](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

Other users will use your **public key** to verify that you, and only you, signed the `Transaction`.

### What's happening when I do a transaction?

You first choose a **public key** to send money to.

Then you create a `Transaction` that will hold the amount you want to send, your **public key**, and the **public key** of the user receiving money.

Then, you print your `Transaction` as a `string`, then you append your **private key** to this `string`, and encode both in *[utf-8](https://en.wikipedia.org/wiki/UTF-8)* format, and hash them. That creates your signature.

> Hashing use [SHA-256 algorithm](https://en.wikipedia.org/wiki/SHA-2)

You then send your `Transaction`, along with your signature and your **public key** to the `Chain`. That is adding a `Block` to the `Chain`.

When the `Chain` receives your demand for adding a new `Block`, it first verifies that your `Transaction` is valid using your **private key** (*so others cannot send money using your identity*).

If your `Transaction` is valid, the `Chain` will **mine** your `Block`, and then add it to the `Chain`.

To **mine** a `Block`, you have to solve a problem. In this example, here is the problem : 
- Each `Block` has a *nonce*, `N`, that is a randomly generated *number* between **0** and **999999999**.
- You have a hash function, `H`, that takes a *number* as input end outputs a *fixed-length string*.
- Let's call `S` the solution to the problem, so `H(S + N)` is a *string* that starts with *0000*.

> `H` is [MD5 algorithm](https://en.wikipedia.org/wiki/MD5)

> The **mining problem** has to be difficult enough to solve. This one can only be solved by random guesses (*[Bitcoin](https://bitcoin.org/bitcoin.pdf)* uses a similar problem).

### Are there problems to solve?

If you have a look at the code, you'll see that the solution to the **mining problem** is never used. That's not how it should be done.

The solution should be added to the `Block` so users will be able to verify that this `Block` has been verified and mined.

> The **mining problem** has to be easy to verify if you have a potential solution at hand. This one only needs one pass, you compute the hash and verify it starts with *0000*.

Moreover, you'll see that you can spend money that you don't have. To avoid that, each time you send a `Transaction`, the `Chain` should calculate the amount of money you have by looking at the previous `Blocks`. Then, if you don't have enough money, your `Transaction` is refused.


# Will cryptocurrency burn the world?

As I've just seen, three important factors impact the energy consumption of cryptocurrencies.
 - **Mining**: the problem to solve cannot be reduced and is solved in parallel by thousands of actors on the network
 - **Memory**: the chain must be saved and duplicated in as many instances as possible
 - **Hardware**: the *Bitcoin* problem is extremely specific and can be solved with specific hardware which changes regularly.

 All in all, the carbon footprint of *Bitcoin* is greater than the one of the **United Arab Emeritas**, and falls just below the Netherlands, with a total of **121.4 TWh per year**.

 New cryptocurrencies are trying to reduce the footprint. They use a *Proof-of-Stake* algorithm instead of the classical *Proof-of-Work* algorithm.

## The source of energy

It is important to consider from where comes the energy when counting for the carbon footprint of **mining**.
Indeed, some places use greener energies than others. For example, there are mining plants near unused energy reserves in China or ones that use *lost methane* from fuel extraction.

However, the act of mining barely follows the schedule imposed by renewable energies such as solar panels or windmills: not all transactions are made on windy sunny days.

Nonetheless, the extensive usage of energy for mining help to reduce the production cost of renewable infrastructure. In 2019, the energy for the mining came at **38% from renewable energies**. That is an **increase** of 10% in one year.

## The material cost

Miners use specialised circuits. First, they used classical CPU. Then they switch for GPU and for **Field Programmable Gate Array** (FGPA) that mines anything. Now, they use a very specialised circuit for *Bitcoin* mining: **Application Specific Integrated Circuits** (ASIC).

The cost-efficiency of these circuits **doubled every 1.5 years**, and it has been the case for the last 65 years. Miners compete: only the first one gets the reward. So, they buy new circuits regularly.

In total, mining hardware e-waste is equivalent to what produces the Netherlands': **32.76kT per year**, without the cooling systems.

To get a sense of scale, that means that **1 *Bitcoin* transaction** has roughly the same e-waste footprint as 2 *iPhone 12*, or **87,500 *VISA* transaction**. However, that goes up to 2,302,133 *VISA* transactions when you consider all types of emission of *Bitcoin*.

