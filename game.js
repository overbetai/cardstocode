<!DOCTYPE html>
<html>
<head>
    <style>
        .poker-table {
            position: relative;
            width: 800px;
            height: 600px;
            margin: 0 auto;
            background: #136713;
            padding: 20px;
        }

        .table-felt {
            position: absolute;
            inset: 20px;
            border-radius: 50%;
            background: #1d8a1d;
            border: 8px solid #654321;
        }

        .community-cards {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            gap: 10px;
        }

        .card {
            background: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 24px;
        }

        .pot {
            position: absolute;
            top: 33%;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 20px;
            font-weight: bold;
        }

        .player {
            position: absolute;
            transform: translate(-50%, -50%);
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            width: 120px;
            text-align: center;
        }

        .player-avatar {
            width: 40px;
            height: 40px;
            background: #ccc;
            border-radius: 50%;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .player-cards {
            display: flex;
            gap: 5px;
            justify-content: center;
            margin-top: 5px;
        }

        .player-position {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div id="poker-table" class="poker-table">
        <div class="table-felt"></div>
    </div>

    <script>
        class PokerTable {
            constructor(containerId) {
                this.container = document.getElementById(containerId);
                this.players = [
                    { id: 1, name: 'Bot 1', chips: 1000, cards: ['🂠', '🂠'], position: 'dealer' },
                    { id: 2, name: 'Bot 2', chips: 1500, cards: ['🂠', '🂠'], position: 'small blind' },
                    { id: 3, name: 'Bot 3', chips: 800, cards: ['🂠', '🂠'], position: 'big blind' },
                    { id: 4, name: 'Bot 4', chips: 2000, cards: ['🂠', '🂠'] },
                    { id: 5, name: 'Bot 5', chips: 1200, cards: ['🂠', '🂠'] },
                    { id: 6, name: 'Bot 6', chips: 900, cards: ['🂠', '🂠'] }
                ];
                this.communityCards = ['🂠', '🂠', '🂠', '🂠', '🂠'];
                this.pot = 150;
                this.init();
            }

            createCommunityCards() {
                const communityCardsDiv = document.createElement('div');
                communityCardsDiv.className = 'community-cards';
                
                this.communityCards.forEach(card => {
                    const cardDiv = document.createElement('div');
                    cardDiv.className = 'card';
                    cardDiv.textContent = card;
                    communityCardsDiv.appendChild(cardDiv);
                });

                this.container.appendChild(communityCardsDiv);
            }

            createPot() {
                const potDiv = document.createElement('div');
                potDiv.className = 'pot';
                potDiv.textContent = `Pot: $${this.pot}`;
                this.container.appendChild(potDiv);
            }

            createPlayers() {
                this.players.forEach((player, index) => {
                    const playerDiv = document.createElement('div');
                    playerDiv.className = 'player';

                    // Calculate position around the table
                    const angle = (index * 360) / this.players.length;
                    const radius = 42; // percentage of container size
                    const x = 50 + radius * Math.cos((angle - 90) * (Math.PI / 180));
                    const y = 50 + radius * Math.sin((angle - 90) * (Math.PI / 180));

                    playerDiv.style.left = `${x}%`;
                    playerDiv.style.top = `${y}%`;

                    // Create player content
                    playerDiv.innerHTML = `
                        <div class="player-avatar">👤</div>
                        <div class="player-name">${player.name}</div>
                        <div class="player-chips">$${player.chips}</div>
                        <div class="player-cards">
                            ${player.cards.map(card => `<div class="card">${card}</div>`).join('')}
                        </div>
                        ${player.position ? `<div class="player-position">${player.position}</div>` : ''}
                    `;

                    this.container.appendChild(playerDiv);
                });
            }

            init() {
                this.createCommunityCards();
                this.createPot();
                this.createPlayers();
            }

            updatePot(amount) {
                this.pot = amount;
                const potDiv = this.container.querySelector('.pot');
                potDiv.textContent = `Pot: $${this.pot}`;
            }

            updatePlayerChips(playerId, amount) {
                const player = this.players.find(p => p.id === playerId);
                if (player) {
                    player.chips = amount;
                    const playerDiv = this.container.querySelector(`.player:nth-child(${playerId + 3})`);
                    playerDiv.querySelector('.player-chips').textContent = `$${amount}`;
                }
            }

            updateCommunityCards(cards) {
                this.communityCards = cards;
                const cardDivs = this.container.querySelectorAll('.community-cards .card');
                cardDivs.forEach((div, index) => {
                    div.textContent = cards[index];
                });
            }
        }

        // Initialize the poker table
        const pokerTable = new PokerTable('poker-table');

        // Example usage:
        // pokerTable.updatePot(300);
        // pokerTable.updatePlayerChips(1, 1200);
        // pokerTable.updateCommunityCards(['🂡', '🂢', '🂣', '🂤', '🂥']);
    </script>
</body>
</html>