class Common:
    
    @staticmethod
    def giveFeedBack(key):
            '''
            Tell user what changes you have made
            '''
            text_values = key.split('_')
            
            display_text  = "Updated"
            for text in text_values:
                display_text += " %s" %text

            display_text += " ..."

            print(display_text)