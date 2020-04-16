describe("FR3 Give offers", function() { 
    it("Sign in and create project with tasks", function() {
        // load authenticated users
        cy.init_test_db()
        cy.login("harrypotter", "Bollerogbrus1_")
        
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/')
        })
        cy.contains('Welcome harrypotter')
        cy.contains('New project').click()

        // fill in title
        cy.get('input[name="title"]').type("My test project")
        // fill in description
        cy.get('textarea[name="description"]').type("My test project description")
        // choose categories
        cy.get('select').select("Cleaning").invoke('val')
        // fill in task title
        cy.get('input[name="task_title"]').type("My test project")
        // fill in budget
        cy.get('input[name="task_budget"]').type(100)
        // fill in description 
        cy.get('textarea[name="task_description"]').type("My test project")

        // click submit
        cy.get('button[type=submit]').click()
    })


    it("Login to see new project, then user makes offer on project, check if email is sent. Check if offer is correct as project owner(FR3, FR4, FR24) ", function() {
        // load authenticated users
        cy.login("harrypotter", "Bollerogbrus1_")
        
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/')
        })
        
        cy.contains('Sign out').click()

        cy.login("admin", "qwerty123")
        cy.get('a[href="/projects/"]').click()
        cy.contains('My test project').click()
        cy.contains('Make Offer').click()
        cy.wait(400)

        const offerTitle = "Offer title";
        const offerDescription = "Offer description";
        const offerPrice = 150;

        cy.get('div[id="makeOfferModal2"]').find('input[name="title"]').type(offerTitle)
        cy.get('div[id="makeOfferModal2"]').find('textarea[name="description"]').type(offerDescription)
        cy.get('div[id="makeOfferModal2"]').find('input[name="price"]').type(offerPrice)
        cy.get('div[id="makeOfferModal2"]').contains('Send Offer').click()
        cy.contains(' Sending email to hp@deskjet.example.com ')
        cy.wait(1500)
        
        cy.contains('Pending')
        

        cy.contains('Sign out').click()
        cy.login("harrypotter", "Bollerogbrus1_")

        cy.contains('My test project - You have 1 pending offers')
        cy.contains('My test project').click()
        cy.contains('View Offer').click()
        cy.get('div[id="seeOfferModal2"]').contains(offerTitle)
        cy.get('div[id="seeOfferModal2"]').contains(offerDescription)
        cy.get('div[id="seeOfferModal2"]').contains(`Price offered: ${offerPrice}`)
    })
})