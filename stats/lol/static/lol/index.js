document.addEventListener('DOMContentLoaded', function() {
    const resultContainer = document.querySelector('#result');
    document.querySelector("#load_anim").style.display = "none";
    document.getElementById('stats-form').addEventListener('submit', async function(event) {
        event.preventDefault();
        resultContainer.innerHTML = '';
        const form = event.target;
        const formData = new FormData(form);
        const data = {
            gameName: formData.get('gameName'),
            tag: formData.get('tag')
        };
        document.querySelector("#load_anim").style.display = "block";
        document.querySelector("#src_btn").disabled = true
        try {
            const response = await fetch('estadistics/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            document.querySelector("#load_anim").style.display = "none";
            document.querySelector("#src_btn").disabled = false;
            console.log(result);
            let cardCount = 10;
            result.participants.forEach(participant => {
                if(cardCount % 10 === 0 && cardCount !== 0)
                    {
                        const partida = document.createElement('h2');
                        partida.textContent = `Partida ${cardCount/10}`;
                        partida.style.width = '100%';
                        resultContainer.appendChild(partida);
                }
                cardCount++;
                const card = document.createElement('div');
                if (participant.win){
                    card.className = "card victory";
                }
                else{
                    card.className = "card defeat";
                }

                card.style.width = "18rem";
                card.innerHTML = `
                <div class="card-body">
                  <h5 class="card-title">${participant.gameName}#${participant.tagLine}</h5>
                  <h6 class="card-subtitle mb-2 text-muted" style="color: antiquewhite !important;">${participant.championName}</h6>
                  <p class="card-text">${participant.role}</p>
                  <a href="#" class="card-link">KDA: ${participant.KDA}</a>
                  <a href="#" class="card-link">${participant.win ? 'Victory' : 'Defeat'}</a>
                </div>`

                resultContainer.appendChild(card);
            });

        } catch (error) {
            console.error('Error fetching match data:', error);
        }
    });
});