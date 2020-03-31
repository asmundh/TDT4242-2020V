describe("FR1 Sign up and Sign in", function() { 
    it("Should register a new user and redirect to /projects", function() {
        // deletes content in database
        cy.init_test_db()

        cy.visit('http://localhost:8000/')
        cy.contains('Sign up').click()

        cy.get('input[name="username"]').type('test-username')
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

    it("Sign in and show home screen", function() {
        cy.visit('http://localhost:8000/')
        cy.contains('Sign in').click()

        cy.get('input[name="username"]').type('harrypotter')
        cy.get('input[name="password"]').type('Bollerogbrus1_')

        cy.get('button[type=submit]').click()
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/')
        })
        cy.contains('Welcome harrypotter')
    })
})