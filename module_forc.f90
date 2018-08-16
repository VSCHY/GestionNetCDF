module module_forc

contains
  subroutine land(dimx, dimy, dimt, dimland, landloc, oldvar, newvar)
! get from land
    IMPLICIT NONE
! Input
    integer(4), intent(in)                        :: dimx, dimy, dimt, dimland
    integer(4), dimension(dimland), intent(in)    :: landloc
    real(4), dimension(dimt, dimland), intent(in) :: oldvar

! Output
    real(4), dimension(dimt, dimy, dimx), intent(out)      :: newvar

! Local 
    integer(4)                                    :: i, ii, jj, t, k

!! Revoir COMMENT SECRIT

    print*, dimt
    DO t=1, dimt
      print*,t
      DO i=1,dimland
          k = landloc(i)/dimx
          if (modulo(landloc(i),dimx)==0) then
            ii = dimx
          else
            ii = landloc(i)-k*dimx
          end if
          jj = k+1
          newvar(t,jj,ii) = oldvar(t,i)
      end do
    end do

  end subroutine land

end module
