/* ==========================================================
   ASSISTANT
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    const textarea = document.querySelector("textarea");

    const submitButton = document.querySelector("button[type='submit']");

    const chatWindow = document.querySelector(".chat-window");

    const suggestionButtons = document.querySelectorAll(".suggestions .btn");

    /* ===========================================
       AUTO SCROLL
    =========================================== */

    if(chatWindow){

        chatWindow.scrollTop = chatWindow.scrollHeight;

    }

    /* ===========================================
       AUTO RESIZE
    =========================================== */

    if(textarea){

        textarea.addEventListener("input", function(){

            this.style.height = "auto";

            this.style.height = this.scrollHeight + "px";

        });

    }

    /* ===========================================
       SUGGESTIONS
    =========================================== */

    suggestionButtons.forEach(button=>{

        button.addEventListener("click",()=>{

            textarea.value = button.textContent.trim();

            textarea.focus();

        });

    });

    /* ===========================================
       ENVOI
    =========================================== */

    if(form){

        form.addEventListener("submit",()=>{

            submitButton.disabled = true;

            submitButton.innerHTML = `

                <span class="spinner-border spinner-border-sm"></span>

                Analyse...

            `;

            if(chatWindow){

                const loading = document.createElement("div");

                loading.className = "message ai-message loading-message";

                loading.innerHTML = `

                    <div class="message-avatar">

                        <i class="bi bi-robot"></i>

                    </div>

                    <div class="message-content">

                        L'assistant analyse votre demande...

                    </div>

                `;

                chatWindow.appendChild(loading);

                chatWindow.scrollTop = chatWindow.scrollHeight;

            }

        });

    }

});