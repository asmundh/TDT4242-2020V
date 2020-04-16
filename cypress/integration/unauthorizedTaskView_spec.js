describe("Visiting a task not logged in should redirect to login page", function() {
    it("should redirect to loginpage when attempting to view a task and not being logged in", function() {
        cy.init_test_db()
        cy.visit('http://localhost:8000/projects/1/tasks/1')
        cy.location().should(loc => {
            expect(loc.href).to.equal('http://localhost:8000/user/login/?next=/projects/1/tasks/1/')
        })
    })
})
