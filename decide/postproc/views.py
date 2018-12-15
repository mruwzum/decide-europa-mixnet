from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def dhondt(self, options, seats):
        #Se añade un campo de escaños (seats) a cada una de las opciones
        for opt in options:
            opt['seats'] = 0

        #Para cada uno de los escaños se calcula a que opción le correspondería el escaño 
        #teniendo en cuenta los ya asignados
        for i in range(seats):
            max(options, 
                key = lambda x : x['votes'] / (x['seats'] + 1.0))['seats'] += 1

        #Se ordenan las opciones por el número de escaños
        options.sort(key=lambda x: -x['seats'])
        return Response(options)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        elif t == 'DHONDT':
            seats = int(float(request.data.get('seats', '8')))
            return self.dhondt(opts,seats)            

        return Response({})
