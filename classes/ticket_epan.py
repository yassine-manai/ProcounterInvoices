class TicketEpanError(Exception):
    pass

class TicketEpan:
    def __init__(self, ticket_epan):
        if not isinstance(ticket_epan, str):
            raise TicketEpanError("ticket_epan must be a string")
        
        if len(ticket_epan) < 18:
            raise TicketEpanError("ticket_epan string is too short")
        
        self.parking = ticket_epan[:2]
        self.clientid = ticket_epan[2:7]
        self.zr_number = ticket_epan[7:11]
        self.season_parker = ticket_epan[11:13]
        self.company_id = ticket_epan[13:18]
        self.ptcpid = ticket_epan[18:]



    def validate(self):
        return (
            self.parking.isdigit() and
            self.clientid.isdigit() and
            self.zr_number.isdigit() and
            self.season_parker.isdigit() and
            self.company_id.isdigit() and
            self.ptcpid.isdigit()  
        )

    def to_dict(self):
        return {
            "parking": self.parking,
            "clientid": self.clientid,
            "zr_number": self.zr_number,
            "season_parker": self.season_parker,
            "company_id": self.company_id,
            "ptcpid": self.ptcpid
        }
