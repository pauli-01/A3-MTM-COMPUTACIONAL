"use strict";

const slides = document.querySelectorAll(".slide");
const navegacao = document.querySelector(".navegacao");
const anterior = document.querySelector("#anterior");
const proximo = document.querySelector("#proximo");
const progresso = document.querySelector("#progresso");
const imprimir = document.querySelector("#imprimir");
let indiceAtual = 0;

// Mantém um slide visível na tela e anuncia sua posição.
function mostrarSlide(indice, moverFoco) {
  if (indice < 0 || indice >= slides.length) {
    return;
  }

  indiceAtual = indice;
  for (let i = 0; i < slides.length; i++) {
    slides[i].hidden = i !== indiceAtual;
  }

  anterior.disabled = indiceAtual === 0;
  proximo.disabled = indiceAtual === slides.length - 1;
  progresso.textContent = `Slide ${indiceAtual + 1} de ${slides.length}`;

  if (moverFoco) {
    slides[indiceAtual].querySelector("h1, h2").focus();
  }
}

anterior.addEventListener("click", () => mostrarSlide(indiceAtual - 1, true));
proximo.addEventListener("click", () => mostrarSlide(indiceAtual + 1, true));
imprimir.addEventListener("click", () => window.print());

// As teclas de edição e os atalhos do navegador continuam disponíveis.
document.addEventListener("keydown", (evento) => {
  if (evento.defaultPrevented || evento.altKey || evento.ctrlKey || evento.metaKey ||
      evento.shiftKey || evento.target.matches("input")) {
    return;
  }

  let destino = indiceAtual;
  switch (evento.key) {
    case "ArrowLeft":
      destino--;
      break;
    case "ArrowRight":
      destino++;
      break;
    case "Home":
      destino = 0;
      break;
    case "End":
      destino = slides.length - 1;
      break;
    default:
      return;
  }

  evento.preventDefault();
  mostrarSlide(destino, true);
});

mostrarSlide(0, false);
navegacao.hidden = false;
