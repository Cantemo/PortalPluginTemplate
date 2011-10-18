import logging
from django.utils.translation import ugettext as _
from portal.vidispine.igeneral import performVSAPICall
from portal.vidispine import signals

from datetime import datetime, timedelta
from portal.vidispine.isearch import SearchHelper
from portal.vidispine.icollection import CollectionHelper
from portal.vidispine.iitem import ItemHelper

log = logging.getLogger(__name__)

#update every 30 seconds
UPDATE_FREQUENCY = 30

"""
This class puts all items visited by all users in a collection called "lastVisitedItems" with a frequency of min 30 seconds.

a) Upon init, make sure there is a collection for last visited items called "lastVisitedItems" with the correct collection type
b) Subscribes to the "vidispine_get_item_ntfcn" signal which is raised everytime the system does the getItem API call to Vidispine
c) When a user visits an item page, put the item id in the items list in the class
d) If last update was over 30 seconds ago, update the collection with the new items and empty the items list
 
"""
class LastVisitedItems(object):
    def __init__(self):
        self.items = []
        self.lastUpdated = datetime.now () - timedelta (seconds = UPDATE_FREQUENCY)
        # Make sure the collection is created, and get the id
        self.collection_id = self.getOrCreateLastVisitedCollectionId()
        # Subscribe to the signal with a callback function
        signals.vidispine_get_item_ntfcn.connect(self.receiver_itempage_visited)
    
    def getOrCreateLastVisitedCollectionId(self):
        """ Attempt to make a search for the 'lastVisitedItems'. If none is found, create it.
        """
        sh = SearchHelper() # don't set the runas, so it is run as admin
        # Set the search domain to collections
        sh.searchdomain = 'collection'
        # Create the searchmetadata where portal_collectiontype_hidden is set to lastVisitedItems
        # Note that Portal doesn't render metadatafields which end with '_hidden'
        sh.searchmetadata = {'fields':{'portal_collectiontype_hidden':{'value':'lastVisitedItems', 'type':'string', 'extradata':{}}}}
        res = performVSAPICall(func=sh.search, args={'_content':{}, 'page':1, 'queryamount':1}, 
                               vsapierror_templateorcode=500)
        if not res['success'] or res['response'][0]['hits'] == 0:
            # Either the search failed or there was no hits for the collection
            return self.createLastVisitedCollection()

    def createLastVisitedCollection(self):
        """ This function is called if there is no last visited collection in the system    
        """
        # Create the collection helper as admin (don't set the runas)
        ch = CollectionHelper()
        # Create a collection with the name lastVisitedItems
        res = performVSAPICall(func=ch.createCollection, args={'collection_name':'lastVisitedItems'},
                               vsapierror_templateorcode=500)
        # If the call fails return
        if not res['success']:
            return
        # Get the ID
        collection_id = res['response'].getId()
        # Update a single metadata field value of the collection
        res = performVSAPICall(func=ch.setCollectionMetadataFieldValue, args={'collection_id':collection_id, 'field_name':'portal_collectiontype_hidden', 'field_val':'lastVisitedItems'},
                               vsapierror_templateorcode=500)
        # Return the collection ID
        return collection_id
    
    def receiver_itempage_visited(self, instance, **kwargs):
        """ The subscriber function to the vidispine_get_item_ntfcn signal
        """
        if not instance in self.items:
            self.items.append(instance)
            
        # Check if it is time to update the last visited collection
        now = datetime.now ()
        if (now - self.lastUpdated) > timedelta (seconds = UPDATE_FREQUENCY):
            log.debug("Time to update!")
            # Setting updated time to now in case something breaks in the API calls - we still want the 30s delay so it doesn't flood the system
            self.lastUpdated = now
            ih = ItemHelper() # run as admin
            # A quick way of adding multiple items to a collection is to create a library of the items and then add the library instead
            res = performVSAPICall(func=ih.createLibraryFromItemList, args={'item_id_list':self.items},
                                   vsapierror_templateorcode=500)
            if not res['success']:
                log.warning("Failed updating last visited items collection. Couldn't create library from item list: %s" % self.items)
                return

            # Get the library ID
            library_id = res['response']
            ch = CollectionHelper() # run as admin
            # Add the library to the collection
            res = performVSAPICall(func=ch.addLibraryToCollection, args={'collection_id':self.collection_id, 'library_id':library_id},
                                   vsapierror_templateorcode=500)
            if not res['success']:
                log.warning("Failed updating last visited items collection. Couldn't add item list to collection: %s" % self.items)
            # Clean the items list
            self.items = []
            log.debug("Updated last visited items successfully")
                
        else:
            log.debug("Not time to update yet...")
            pass

lastVisitedItems = LastVisitedItems()

