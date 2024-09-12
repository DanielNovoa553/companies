function loadCompanies() {
    fetch('/get_companies/')
        .then(response => response.json())
        .then(data => {
            $('#companies').DataTable({
                destroy: true,
                data: data.companies, // Asegúrate de que data.companies sea un array de objetos
                columns: [
                    {
                        data: null,
                        render: function(data, type, row, meta) {
                            return meta.row + 1; // Número secuencial
                        }
                    },
                    { data: 'id' },
                    { data: 'name' },
                    { data: 'description' },
                    { data: 'symbol' },
                    {
                        data: null,
                        render: function(data, type, row) {
                            return `
                                <ul class="navbar-nav me-4 mb-2 mb-lg-0">
                                    <li class="nav-item d-flex">
                                        <a class="nav-link ms-2" href="#" title="" onclick="seeCompany('${data.id}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-eye" viewBox="0 0 16 16">
                                                    <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                                                    <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                                </svg>
                                            </a>

                                        <a class="nav-link ms-4" href="#" title="" onclick="seeEditCompany('${data.id}')">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="Green" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                            </svg>
                                        </a>
                                        <a class="nav-link ms-4" href="#" title="Eliminar compañía" onclick="deleteCompany('${data.id}')">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" class="bi bi-trash" viewBox="0 0 16 16">
                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1 1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                            </svg>
                                        </a>
                                    </li>
                                    <li class="nav-item"></li>
                                </ul>
                            `;
                        }
                    }
                ],
                language: {
                    lengthMenu: "Mostrar _MENU_ registros por página",
                    zeroRecords: "No se encontraron resultados",
                    info: "Mostrando página _PAGE_ de _PAGES_",
                    infoEmpty: "No hay registros disponibles",
                    infoFiltered: "(filtrado de _MAX_ registros totales)",
                    search: "Buscar:",
                    paginate: {
                        first: "Primero",
                        last: "Último",
                        next: "Siguiente",
                        previous: "Anterior"
                    }
                },
                order: [[0, "asc"]],
                columnDefs: [
                    { orderable: false, targets: [5] } // Ajusta el índice para la columna de acciones
                ]
            });
        })
        .catch(error => console.error('Error:', error));
}
   function seeCompany(id) {
    fetch(`/get_company/${id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Mostrar los datos en un modal
            $('#companyModal .modal-body').html(`
                <p>ID: ${data.id}</p>
                <p>Name: ${data.name}</p>
                <p>Description: ${data.description}</p>
                <p>Symbol: ${data.symbol}</p>
            `);
            $('#companyModal').modal('show');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

    function seeEditCompany(id) {
    fetch(`/get_company/${id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Mostrar los datos en un modal para editar
            $('#editCompanyModal .modal-body').html(`
                <form id="editCompanyForm">
                    <div class="mb-3">
                        <label for="editCompanyName" class="form-label">Name</label>
                        <input type="text" class="form-control" id="editCompanyName" value="${data.name}">
                    </div>
                    <div class="mb-3">
                        <label for="editCompanyDescription" class="form-label">Description</label>
                        <input type="text" class="form-control" id="editCompanyDescription" value="${data.description}">
                    </div>
                    <div class="mb-3">
                        <label for="editCompanySymbol" class="form-label">Symbol</label>
                        <input type="text" class="form-control" id="editCompanySymbol" value="${data.symbol}">
                    </div>
                    <input type="hidden" id="editCompanyId" value="${data.id}">

                    <div class="d-flex justify-content-center">
                        <button type="button" class="btn btn-success me-2" onclick="updateCompany()">Actualizar</button>
                        <button type="button" class="btn btn-danger" id="cancel" data-bs-dismiss="modal">Cancelar</button>
                    </div>
                </form>
            `);
            $('#editCompanyModal').modal('show');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function updateCompany() {
    const id = $('#editCompanyId').val();
    const name = $('#editCompanyName').val();
    const description = $('#editCompanyDescription').val();
    const symbol = $('#editCompanySymbol').val();

    fetch(`/update_company/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
        },
        body: JSON.stringify({
            name: name,
            description: description,
            symbol: symbol
        })
    })
    .then(response => response.json()
        .then(data => {
            if (response.ok) {
                $('#editCompanyModal').modal('hide');
                loadCompanies();  // Refresh the companies table
            } else {
                // Show server validation error message
                showErrorModal(data.error || 'Something went wrong');
            }
        })
    )
    .catch(error => {
        showErrorModal(error.message);  // Display error in a modal
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

 function showErrorModal(message) {
    document.getElementById('errorModalBody').innerText = message;
    $('#errorModal').modal('show');
}

    function cleanForm() {
    document.getElementById('companyForm').reset();
}

    function showAddCompanyModal() {
    $('#modalAddCompany').modal('show');
}

document.getElementById('companyForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene el envío del formulario por defecto

    if (this.checkValidity()) { // Verifica si el formulario es válido
        addCompany();
    } else {
        this.reportValidity(); // Muestra los mensajes de validación
    }
});

function addCompany() {
    const name = $('#nombre').val();
    const description = $('#descripcion').val();
    const symbol = $('#simbolo').val();

    fetch('/add_company/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Asegúrate de incluir el token CSRF
        },
        body: JSON.stringify({
            name: name,
            description: description,
            symbol: symbol
        })
    })
    .then(response => response.json()
        .then(data => {
            if (response.ok) {
                $('#modalAddCompany').modal('hide');
                loadCompanies();  // Refresca la tabla de compañías
            } else {
                showErrorModal(data.error || 'Something went wrong');
            }
        })
    )
    .catch(error => {
        showErrorModal(error.message);  // Muestra el error en un modal
    });
}

function deleteCompany(id) {
    if (confirm('Are you sure you want to delete this company?')) {
        fetch(`/delete_company/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token if necessary
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(error => {
                    throw new Error(error.message || 'Something went wrong');
                });
            }
        })
        .then(data => {
             $('#successModal').modal('hide');
            showSuccessModal('Empresa eliminada correctamente');
            loadCompanies();  // Refresh the companies table
        })
        .catch(error => {
            showErrorModal(error.message);  // Display error in a modal
        });
    }
}

function showSuccessModal(message) {
document.getElementById('successModalBody').innerText = message;
$('#successModal').modal('show');
}