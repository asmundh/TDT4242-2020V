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


    it("Login to see new project", function() {
        // load authenticated users
        cy.login("harrypotter", "Bollerogbrus1_")
        
        cy.location().should((loc) => {
            expect(loc.href).to.equal('http://localhost:8000/')
        })
        cy.contains('My test project')

    })
})