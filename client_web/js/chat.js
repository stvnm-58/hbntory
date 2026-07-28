function appendMessage(role, text) {
  const thread = document.getElementById("chat-thread");

  const bubble = document.createElement("div");
  bubble.className = `bubble bubble--${role}`;

  const p = document.createElement("p");
  p.textContent = text;

  bubble.appendChild(p);
  thread.appendChild(bubble);
  thread.scrollTop = thread.scrollHeight;
  return bubble;
}

function appendLoadingBubble() {
  const thread = document.getElementById("chat-thread");

  const bubble = document.createElement("div");
  bubble.className = "bubble bubble--loading";

  const p = document.createElement("p");
  p.setAttribute("aria-label", "L'assistant réfléchit");
  for (let i = 0; i < 3; i += 1) {
    const dot = document.createElement("span");
    dot.className = "typing-dot";
    p.appendChild(dot);
  }

  bubble.appendChild(p);
  thread.appendChild(bubble);
  thread.scrollTop = thread.scrollHeight;
  return bubble;
}

function resolveBubble(bubble, role, text) {
  bubble.className = `bubble bubble--${role}`;
  bubble.innerHTML = "";

  const p = document.createElement("p");
  p.textContent = text;
  bubble.appendChild(p);

  const thread = document.getElementById("chat-thread");
  thread.scrollTop = thread.scrollHeight;
}

const AI_SERVICE_URL = "http://localhost:8000";

async function askBot(question) {
  const response = await fetch(`${AI_SERVICE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error(`Erreur du service IA (code ${response.status})`);
  }

  const data = await response.json();
  return data.answer;
}

document.addEventListener("DOMContentLoaded", () => {
  const bubble = document.getElementById("chat-bubble");
  const panel = document.getElementById("chat-panel");
  const closeBtn = document.getElementById("chat-panel-close");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");

  const EDGE_MARGIN = 20;
  const DRAG_THRESHOLD = 6;

  let dragging = false;
  let moved = false;
  let pointerId = null;
  let startX = 0;
  let startY = 0;
  let bubbleStartX = 0;
  let bubbleStartY = 0;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function placeBubbleAt(x, y) {
    const rect = bubble.getBoundingClientRect();
    const maxX = window.innerWidth - rect.width - EDGE_MARGIN;
    const maxY = window.innerHeight - rect.height - EDGE_MARGIN;

    bubble.style.left = `${clamp(x, EDGE_MARGIN, maxX)}px`;
    bubble.style.top = `${clamp(y, EDGE_MARGIN, maxY)}px`;
    bubble.style.right = "auto";
    bubble.style.bottom = "auto";
  }

  function snapToNearestEdge() {
    const rect = bubble.getBoundingClientRect();
    const onLeft = rect.left + rect.width / 2 < window.innerWidth / 2;
    const top = clamp(rect.top, EDGE_MARGIN, window.innerHeight - rect.height - EDGE_MARGIN);

    bubble.style.top = `${top}px`;
    bubble.style.bottom = "auto";
    bubble.style.left = onLeft ? `${EDGE_MARGIN}px` : "auto";
    bubble.style.right = onLeft ? "auto" : `${EDGE_MARGIN}px`;

    if (!panel.hidden) positionPanel();
  }

  function positionPanel() {
    const rect = bubble.getBoundingClientRect();
    const onLeft = rect.left + rect.width / 2 < window.innerWidth / 2;
    const gap = 12;

    // Ouvre du côté (au-dessus ou en dessous de la bulle) qui a le plus de
    // place, et adapte la hauteur du panneau pour ne jamais chevaucher la bulle.
    const spaceAbove = rect.top - EDGE_MARGIN - gap;
    const spaceBelow = window.innerHeight - rect.bottom - EDGE_MARGIN - gap;
    const openAbove = spaceAbove >= spaceBelow;
    const panelHeight = clamp(openAbove ? spaceAbove : spaceBelow, 200, 440);
    panel.style.height = `${panelHeight}px`;

    const panelWidth = panel.offsetWidth;
    let left = onLeft ? rect.left : rect.right - panelWidth;
    left = clamp(left, EDGE_MARGIN, window.innerWidth - panelWidth - EDGE_MARGIN);

    const top = openAbove ? rect.top - panelHeight - gap : rect.bottom + gap;

    panel.style.left = `${left}px`;
    panel.style.top = `${top}px`;
    panel.style.right = "auto";
    panel.style.bottom = "auto";
  }

  function openPanel() {
    panel.hidden = false;
    positionPanel();
    bubble.setAttribute("aria-expanded", "true");
    input.focus();
  }

  function closePanel() {
    panel.hidden = true;
    bubble.setAttribute("aria-expanded", "false");
  }

  function togglePanel() {
    if (panel.hidden) {
      openPanel();
    } else {
      closePanel();
    }
  }

  // Position de départ : coin inférieur droit.
  placeBubbleAt(
    window.innerWidth - bubble.offsetWidth - EDGE_MARGIN,
    window.innerHeight - bubble.offsetHeight - EDGE_MARGIN
  );
  snapToNearestEdge();

  bubble.addEventListener("pointerdown", (event) => {
    dragging = true;
    moved = false;
    pointerId = event.pointerId;
    bubble.setPointerCapture(pointerId);

    const rect = bubble.getBoundingClientRect();
    startX = event.clientX;
    startY = event.clientY;
    bubbleStartX = rect.left;
    bubbleStartY = rect.top;
  });

  bubble.addEventListener("pointermove", (event) => {
    if (!dragging || event.pointerId !== pointerId) return;

    const dx = event.clientX - startX;
    const dy = event.clientY - startY;
    if (Math.abs(dx) > DRAG_THRESHOLD || Math.abs(dy) > DRAG_THRESHOLD) {
      moved = true;
    }
    placeBubbleAt(bubbleStartX + dx, bubbleStartY + dy);
  });

  function endDrag(event) {
    if (!dragging || event.pointerId !== pointerId) return;
    dragging = false;
    bubble.releasePointerCapture(pointerId);

    if (moved) {
      snapToNearestEdge();
    } else {
      togglePanel();
    }
  }

  bubble.addEventListener("pointerup", endDrag);
  bubble.addEventListener("pointercancel", endDrag);

  closeBtn.addEventListener("click", closePanel);

  window.addEventListener("resize", () => {
    snapToNearestEdge();
  });

  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    appendMessage("user", question);
    input.value = "";
    input.disabled = true;
    submitButton.disabled = true;

    const loadingBubble = appendLoadingBubble();

    try {
      const answer = await askBot(question);
      resolveBubble(loadingBubble, "bot", answer);
    } catch (error) {
      resolveBubble(
        loadingBubble,
        "error",
        "Désolé, l'assistant est indisponible pour le moment. Réessayez dans un instant."
      );
    } finally {
      input.disabled = false;
      submitButton.disabled = false;
      input.focus();
    }
  });
});
