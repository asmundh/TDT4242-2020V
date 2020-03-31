describe("Registration tests", function() {
    before(function() {
        cy.exec('rm -r db.sqlite3')
        cy.exec('python manage.py migrate')
        cy.exec('python manage.py loaddata seed.json')
    })

    it("Should register a new user and redirect to /projects", function() {
        cy.visit('http://localhost:8000/')
        cy.contains('Sign up').click()

        cy.get('input[name="username"]').type('TestUsername5')
        cy.get('input[name="first_name"]').type('Test firstname')
        cy.get('input[name="last_name"]').type('Test lastname')
        cy.get('select').select(["Cleaning", "Gardening"]).invoke('val')
        cy.get('input[name="company"]').type('Test company')
        cy.get('input[name="email"]').type('testuser@hotmail.com')
        cy.get('input[name="email_confirmation"]').type('testuser@hotmail.com')
        cy.get('input[name="password1"]').type('Bollerogbrus1_')
        cy.get('input[name="password2"]').type('Bollerogbrus1_')
        cy.get('input[name="phone_number"]').type('54912020')
        cy.get('input[name="country"]').type('Norway')
        cy.get('input[name="state"]').type('Norway')
        cy.get('input[name="city"]').type('Trondheim')
        cy.get('input[name="postal_code"]').type('7034')
        cy.get('input[name="street_address"]').type('Trondheimsvegen 20')

        cy.get('button[type=submit]').click()
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/projects/')
        })
        cy.contains('Your account has been created and is awaiting verification.')
    })

    it("Should not register a user if username is taken", function() {
        cy.visit('http://localhost:8000/')
        cy.contains('Sign up').click()

        cy.get('input[name="username"]').type('TestUsername5')
        cy.get('input[name="first_name"]').type('Test firstname')
        cy.get('input[name="last_name"]').type('Test lastname')
        cy.get('select').select(["Cleaning", "Gardening"]).invoke('val')
        cy.get('input[name="company"]').type('Test company')
        cy.get('input[name="email"]').type('testuser@hotmail.com')
        cy.get('input[name="email_confirmation"]').type('testuser@hotmail.com')
        cy.get('input[name="password1"]').type('Bollerogbrus1_')
        cy.get('input[name="password2"]').type('Bollerogbrus1_')
        cy.get('input[name="phone_number"]').type('54912020')
        cy.get('input[name="country"]').type('Norway')
        cy.get('input[name="state"]').type('Norway')
        cy.get('input[name="city"]').type('Trondheim')
        cy.get('input[name="postal_code"]').type('7034')
        cy.get('input[name="street_address"]').type('Trondheimsvegen 20')

        cy.get('button[type=submit]').click()
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/user/signup/')
        })
        cy.contains('A user with that username already exists.')
    })

    it("should accept a new user from admin panel", function() {
        cy.visit('http://localhost:8000/user/login/')
        cy.get('input[name="username"]').type('TestUsername5')
        cy.get('input[name="password"]').type('Bollerogbrus1_')        
        cy.get('button[type="submit"]').click()
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/user/login/')
        })
        cy.contains('Please enter a correct username and password. Note that both fields may be case-sensitive.')


        cy.visit('http://localhost:8000/admin')

        cy.get('input[name="username"]').type('admin')
        cy.get('input[name="password"]').type('qwerty123')

        cy.get('input[type=submit]').click()
        cy.contains('Users').click()
        cy.get('input[name="form-2-is_active"]').should('have.prop', 'checked')
        cy.get('input[name="form-0-is_active"]').should('not.be.checked')

        cy.get('input[name="form-0-is_active"]').click()
        cy.get('input[name="_save"]').click()
        cy.get('input[name="form-0-is_active"]').should('have.prop', 'checked')

        cy.visit('http://localhost:8000/user/login/')
        cy.get('input[name="username"]').type('TestUsername5')
        cy.get('input[name="password"]').type('Bollerogbrus1_')        
        cy.get('button[type="submit"]').click()
    })
})