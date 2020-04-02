


// Joe has project

// Admin makes offer on project

// Joe accepts said offer

// Admin views said offer and it has been accepted.

// Log into joe and view both offers made by admin. Accept these.

describe("Test that project owner should be able to accept offers", function() {
    
    const seedFileName = 'fr5_seed.json'

    before(function() {
        cy.init_db_by_seed(seedFileName)
    })

    it("Should log into project owner and accept both bids given on tasks", function() {
        cy.login("joe", "qwerty123")
        cy.contains('Projects').click()
        cy.contains('Posted by: joe').click()
        cy.get('button[data-target="#seeOfferModal2"]').click()
        cy.wait(500)
        cy.get('div[id="seeOfferModal2"]  div[class="modal-content"] select').select('Accepted').invoke('val')
        cy.get('div[id="seeOfferModal2"]  div[class="modal-content"] textarea').type('Excited to see how this will turn out!')
        cy.get('div[id="seeOfferModal2"]  div[class="modal-content"] button[name="offer_response"]').click()

        cy.get('button[data-target="#seeOfferModal3"]').click()
        cy.wait(500)
        cy.get('div[id="seeOfferModal3"]  div[class="modal-content"] select').select('Accepted').invoke('val')
        cy.get('div[id="seeOfferModal3"]  div[class="modal-content"] textarea').type('Excited to see how this will turn out!')
        cy.get('div[id="seeOfferModal3"]  div[class="modal-content"] button[name="offer_response"]').click()
    })
})