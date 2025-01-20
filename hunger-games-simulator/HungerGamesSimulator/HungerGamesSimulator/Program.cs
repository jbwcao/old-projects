namespace HungerGamesSimulator
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args is null)
            {
                throw new ArgumentNullException(nameof(args));
            }

            int dayKills;
            int numOfPlayers = 0;

            Console.WriteLine("Welcome to the Hunger Games Simulator");
            Console.WriteLine("May the odds be ever in your favor");
            Console.WriteLine();
            Console.WriteLine("THE REAPING");

            for (bool playerSet = false; playerSet == false;)
            {
                try
                {
                    Console.Write("Enter the number of tribute: ");
                    numOfPlayers = Convert.ToInt32(Console.ReadLine());
                    playerSet = true;
                    if (numOfPlayers < 1)
                    {
                        Console.WriteLine("Invalid Input, try again");
                        playerSet = false;
                    }
                }

                catch
                {
                    Console.WriteLine("Invalid Input, try again");
                }
            }

            bool summariesEnabled;
            Console.WriteLine("Include end of day summaries? [Y/N]");
            if (Console.ReadLine() == "Y")
            {
                summariesEnabled = true;
            }
            else
            {
                summariesEnabled = false;
            }

            int counter = 1;
            List<Tribute> playerList = new();
            for (int i = 0; i < numOfPlayers; i++)
            {

                Console.WriteLine("Enter the name of the " + counter + getPlacement(counter) + " player");

                try
                {
                    playerList.Add(new Tribute(Console.ReadLine(), true, 0));
                }

                catch
                {
                    Console.WriteLine("Exception Thrown");
                }

                counter++;

            }

            Console.WriteLine();
            Console.WriteLine("Let the games begin!");
            Console.WriteLine();

            var random = new Random(Guid.NewGuid().GetHashCode());

            int day = 0;
            int playersAlive = playerList.Count;

            while (playersAlive != 1)
            {

                dayKills = Convert.ToInt32(playersAlive / random.Next(2, 3));
                day++;
                Console.WriteLine($"Day {day}");

                Tribute killer;
                Tribute deadPlayer;

                for (; dayKills > 0; dayKills--)
                {
                    do
                    {
                        killer = playerList[random.Next(0, playerList.Count)];
                    } while (killer.isTributeAlive == false);

                    do
                    {
                        deadPlayer = playerList[random.Next(0, playerList.Count)];

                    } while (deadPlayer.isTributeAlive == false);

                    deadPlayer.isTributeAlive = false;

                    if (deadPlayer == killer)
                    {
                        Console.WriteLine(getSelfDeathMessage(deadPlayer.tributeName));
                    }
                    else
                    {
                        Console.WriteLine($"{deadPlayer.tributeName} is killed by {killer.tributeName}");
                        killer.tributeKills++;
                    }

                    playersAlive--;
                }

                if (summariesEnabled)
                {
                    Console.WriteLine();
                    Console.WriteLine("Current Standings");

                    foreach (Tribute tribute in playerList)
                    {
                        Console.WriteLine($"Name: {tribute.tributeName}  Status: {GetDeadorAlive(tribute.isTributeAlive)}  Kills: {tribute.tributeKills}");
                    }
                }
                Console.WriteLine();
            }

            Tribute? victor = null;
            for (int i = 0; i <= playerList.Count - 1; i++)
            {
                if (playerList[i].isTributeAlive == true)
                {
                    victor = playerList[i];
                }
            }
            
            if (victor != null)
            {
                Console.WriteLine($"{victor.tributeName} is the victor with {victor.tributeKills} kills");
            }
            else
            {
                Console.WriteLine("[Debug] No Victor");
            }

            Console.WriteLine();
            Console.WriteLine("Kill Counts");

            foreach (Tribute tribute in playerList)
            {
                Console.WriteLine($"{tribute.tributeName}: {tribute.tributeKills}");
            }

            static string getPlacement(int num)
            {
                string placementName = num switch
                {
                    1 or 21 or 31 or 41 or 51 or 61 or 71 or 81 or 91 => "st",
                    2 or 22 or 32 or 42 or 52 or 62 or 72 or 82 or 92 => "nd",
                    3 or 23 or 33 or 43 or 53 or 63 or 73 or 83 or 93 => "rd",
                    _ => "th",
                };
                return placementName;
            }

            string getSelfDeathMessage(string name)
            {
                var random = new Random(Guid.NewGuid().GetHashCode());
                int randomInt;


                if (day < 2)
                {
                    randomInt = random.Next(1, 9);
                }
                else if (day < 5)
                {

                    randomInt = (int)random.Next(1, 9);
                }
                else
                {
                    randomInt = (int)random.Next(1, 11);

                }

                string deathMessage = randomInt switch
                {

                    1 => $"{name} fell out of a tree and died",
                    2 => $"{name} died to exposure",
                    3 => $"{name} was mauled to death by wolves",
                    4 => $"{name} was eaten by hungry aligators trying to cross a river",
                    5 => $"{name} died to poisionous berries",
                    6 => $"{name} died to a tracker jacker sting",
                    7 => $"{name} bid farewell to this cruel world",
                    8 => $"{name} dies to their own trap",
                    9 => $"{name} tested for fall damage",
                    10 => $"{name} dies of thirst",
                    11 => $"{name} dies of starvation",

                    _ => "[Debug]switch statement error you failure Jonathan"
                };
                return deathMessage;
            }

            static string GetDeadorAlive(bool status)
            {
                if (status == true)
                {
                    return "Alive";
                }
                else
                {
                    return "Dead";
                }
            }
        }

        public class Tribute
        {

            public string? tributeName;
            public bool isTributeAlive;
            public int tributeKills;

            public Tribute(string aTributeName, bool startIsTributeAlive, int startTributeKills)
            {
                tributeName = aTributeName;
                isTributeAlive = startIsTributeAlive;
                tributeKills = startTributeKills;
            }
        }
    }
}
