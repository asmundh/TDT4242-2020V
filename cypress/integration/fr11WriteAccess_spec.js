describe("Tests that users with read access should be able to upload files", function() {

    const seedFileName = "fr11_seed.json"
    it("Should be possible for task owner to upload file", function() {
        cy.init_db_by_seed(seedFileName)
        cy.login("joe", "qwerty123")
        cy.wait
        cy.contains('My Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.get('a[href="/projects/2/tasks/2/upload/"]').click()
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.contains('Upload File').click()
    })

    it("Should be possible for task manager to upload file", function() {
        cy.init_db_by_seed(seedFileName)
        cy.login("admin", "qwerty123")
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.get('a[href="/projects/2/tasks/2/upload/"]').click()
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.contains('Upload File').click()
        cy.contains('Sign out').click()
    })

    it("should be possible for task participant to upload file", function() {
        cy.init_db_by_seed(seedFileName)
        cy.login("harrypotter", "qwerty123")
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.get('a[href="/projects/2/tasks/2/upload/"]').click()
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.contains('Upload File').click()
    })
})
