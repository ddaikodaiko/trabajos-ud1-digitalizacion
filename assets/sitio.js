// Menú en pantallas pequeñas
(function () {
  var rail = document.querySelector(".rail");
  var boton = document.querySelector(".menu-boton");
  if (!rail || !boton) return;
  boton.addEventListener("click", function () {
    var abierto = rail.getAttribute("data-abierto") === "true";
    rail.setAttribute("data-abierto", abierto ? "false" : "true");
    boton.setAttribute("aria-expanded", abierto ? "false" : "true");
  });
})();

// Demostración del seguimiento de un pedido (Punto 6)
(function () {
  var caja = document.getElementById("seguimiento");
  if (!caja) return;

  var pasos = [
    {
      titulo: "Pedido recibido",
      cliente: "Hemos recibido tu pedido de 120 sudaderas con tu logotipo bordado. Te confirmamos la fecha de entrega calculada con la carga actual del taller.",
      entorno: "IT",
      origen: "La tienda online crea el pedido en el sistema de gestión y este reserva las prendas en el inventario."
    },
    {
      titulo: "Diseño validado",
      cliente: "Tu diseño está listo. Has aprobado la prueba en pantalla y ya no admite cambios.",
      entorno: "IT",
      origen: "Diseño revisa el archivo y lo adjunta al pedido. La aprobación del cliente queda registrada."
    },
    {
      titulo: "En cola de producción",
      cliente: "Tu pedido está en la cola del taller. Tiene dos trabajos por delante.",
      entorno: "IT → OT",
      origen: "El módulo de fabricación genera la orden con su código QR y la envía a la tableta de bordado junto con el diseño."
    },
    {
      titulo: "En bordado",
      cliente: "Estamos bordando tu pedido: 45 de 120 sudaderas terminadas.",
      entorno: "OT",
      origen: "El operario ha escaneado el QR al empezar. La máquina de bordado conectada cuenta las unidades."
    },
    {
      titulo: "Control de calidad",
      cliente: "Bordado terminado. Estamos revisando y empaquetando las prendas.",
      entorno: "OT",
      origen: "En la tableta de acabado se marcan las unidades correctas. Dos se repiten y el material se descuenta del inventario."
    },
    {
      titulo: "Enviado",
      cliente: "Tu pedido ha salido del taller. Aquí tienes el enlace de seguimiento del transporte y tu factura.",
      entorno: "OT → IT",
      origen: "Almacén escanea la salida. El sistema emite la factura y envía el aviso al cliente sin que nadie escriba un correo."
    }
  ];

  var lista = caja.querySelector(".hitos-seg");
  var titulo = caja.querySelector("[data-campo='titulo']");
  var cliente = caja.querySelector("[data-campo='cliente']");
  var entorno = caja.querySelector("[data-campo='entorno']");
  var origen = caja.querySelector("[data-campo='origen']");
  var siguiente = caja.querySelector("[data-accion='siguiente']");
  var reiniciar = caja.querySelector("[data-accion='reiniciar']");
  var actual = 0;

  pasos.forEach(function (p) {
    var li = document.createElement("li");
    li.textContent = p.titulo;
    lista.appendChild(li);
  });

  function etiqueta(texto) {
    var clase = texto === "IT" ? "et--it" : texto === "OT" ? "et--ot" : "et--mix";
    return '<span class="et ' + clase + '">' + texto + "</span>";
  }

  function pintar() {
    var p = pasos[actual];
    Array.prototype.forEach.call(lista.children, function (li, i) {
      li.setAttribute("data-hecho", i < actual ? "true" : "false");
      li.setAttribute("data-actual", i === actual ? "true" : "false");
    });
    titulo.textContent = p.titulo;
    cliente.textContent = p.cliente;
    entorno.innerHTML = etiqueta(p.entorno);
    origen.textContent = p.origen;
    siguiente.disabled = actual === pasos.length - 1;
    siguiente.textContent = actual === pasos.length - 1 ? "Pedido entregado al transporte" : "Avanzar al siguiente estado";
  }

  siguiente.addEventListener("click", function () {
    if (actual < pasos.length - 1) { actual += 1; pintar(); }
  });
  reiniciar.addEventListener("click", function () { actual = 0; pintar(); });
  pintar();
})();

// Fotos: si alguna no llega a cargar, se retira sin descolocar la página
(function () {
  var fotos = document.querySelectorAll("img[data-foto]");
  function retirar(img) {
    var banda = img.closest(".foto-banda");
    if (banda) { banda.hidden = true; return; }
    var tarjeta = img.closest(".entorno");
    if (tarjeta) tarjeta.classList.add("tarjeta--sin-foto");
  }
  for (var i = 0; i < fotos.length; i++) {
    (function (img) {
      img.addEventListener("error", function () { retirar(img); });
      if (img.complete && img.currentSrc && img.naturalWidth === 0) retirar(img);
    })(fotos[i]);
  }
})();
