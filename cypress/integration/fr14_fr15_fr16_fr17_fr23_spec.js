describe("Feedback and project status tests", function() {

    const seedFileName = 'fr14_seed.json'

    before(function() {
        cy.init_db_by_seed(seedFileName)
    })

    it("Should log into customer account and review their delivery(FR14, FR16, FR17, FR23", function() {
        cy.login('joe', 'qwerty123')
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.contains('Respond').click()

        cy.get('select[id="id_status"]').select('Accepted').invoke('val')
        cy.get('textarea[id="id_feedback"]').type('Supert smupert!')
        cy.wait(200)
        cy.get('input[id="id_rating"]').type(4)
        cy.contains('Send Response').click()

        cy.contains('Pay').click()

        cy.get('input[id="id_cardnumber"]').type('123948172')
        cy.get('input[id="id_expirymonth"]').type('08')
        cy.get('input[id="id_expiryyear"]').type('21')
        cy.get('input[id="id_cvc"]').type('314')
        cy.get('button[type="submit"]').click()

        cy.visit('http://localhost:8000/user/admin/')
        cy.get('div[id="rating"]').contains(4.0)
        cy.contains('1 REVIEWS')
    })

    it('Should give poor feedback on project, and project manager must review feedback(FR 15)', function() {
        cy.init_db_by_seed(seedFileName)
        cy.login('joe', 'qwerty123')
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()
        cy.contains('Respond').click()

        cy.get('select[id="id_status"]').select('Declined').invoke('val')
        cy.get('textarea[id="id_feedback"]').type('Ikke bra nok ass!')
        cy.wait(200)
        cy.get('input[id="id_rating"]').type(2)
        cy.contains('Send Response').click()
        cy.contains('Sign out').click()


        cy.login('admin', 'qwerty123')
        cy.contains('Costumer Projects').click()
        cy.contains('FR5 Clean my ship').click()
        cy.get('a[href="/projects/2/tasks/2/"]').click()

        cy.contains('Ikke bra nok ass!')
        cy.contains('Declined')

        cy.contains(/\bDeliver\b/).click()
        cy.wait(600)
        cy.get('div[id="seeDeliverModal"] textarea[name="comment"]').type('This is not it, this is just a comment')
        cy.get('input[type="file"]').attachFile('../seeds/fr5_seed.json')
        cy.get('div[id="seeDeliverModal"]').contains('Deliver').click()
        cy.contains('Status: Pending')

    })
})
