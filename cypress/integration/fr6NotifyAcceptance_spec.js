describe("Test that project owner should be able to accept offers", function() {
    
    const seedFileName = 'fr6_seed.json'

    before(function() {
        cy.init_db_by_seed(seedFileName)
    })

    it("Should click deliver and add a role", function() {
        cy.login("admin", "qwerty123")
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()

        cy.get('button').contains("Add Role").click()
        cy.wait(400)
        cy.get('input[name="name"]').type('Administering')
        cy.get('div[id="seeTeamModal"]').contains('Add Role').click()

        cy.wait(300)
        cy.contains('User').click()
        cy.get('div[id="seeTeamAddModal1"] select').select('harrypotter').invoke('val')
        cy.get('div[id="seeTeamAddModal1"]').contains('Add Members').click()

        cy.contains('Change permissions').click()
        cy.get('input[name="permission-upload-1"]').check()
        cy.get('div[id="seePermissionModal"]').contains('Change permissions').click()


    })
})
// cy.contains(/\bDeliver\b/).click()